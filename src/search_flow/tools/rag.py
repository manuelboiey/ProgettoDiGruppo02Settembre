"""Strumento RAG per interrogare documenti locali con citazioni.

Questo modulo definisce lo strumento `RAG` basato su FAISS e LangChain per
supportare retrieval-augmented generation sui documenti locali, inclusa la
gestione della persistenza dell'indice e la costruzione della catena di
prompting con citazioni delle fonti.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import List, ClassVar, Any, Iterable, Tuple

from crewai.tools import BaseTool
from dotenv import load_dotenv

from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import AzureOpenAIEmbeddings
from langchain_openai import AzureChatOpenAI

# LangChain Core (prompt/chain)
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Qdrant vector database client and models
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    HnswConfigDiff,
    OptimizersConfigDiff,
    ScalarQuantization,
    ScalarQuantizationConfig,
    PayloadSchemaType,
    FieldCondition,
    MatchValue,
    MatchText,
    Filter,
    SearchParams,
    PointStruct,
)




@dataclass
class Settings:
    """Parametri di configurazione per vettorizzazione e retrieval."""
    # Text splitting
    chunk_size: int = 1500
    chunk_overlap: int = 300
    # Retriever (MMR)
    mmr_lambda: float = 0.6         # 0 = diversificazione massima, 1 = pertinenza massima
    
    # =========================
    # Qdrant Vector Database Configuration
    # =========================
    qdrant_url: str = "http://localhost:6333"
    collection: str = "rag_chunks"
    
    # =========================
    # Hybrid Search Configuration
    # =========================
    top_n_semantic: int = 30
    top_n_text: int = 100
    final_k: int = 6  
    alpha: float = 0.75
    text_boost: float = 0.20
    
    # =========================
    # MMR (Maximal Marginal Relevance) Configuration
    # =========================
    use_mmr: bool = True
    



class RAG(BaseTool):
    """Tool RAG per interrogare documenti locali e rispondere con citazioni."""

    name: str = "RAG"
    description: str = "Uno strumento per cercare risultati sui documenti"

    # Usa ClassVar per indicare che è una variabile di classe, non un campo del modello
    SETTINGS: ClassVar[Settings] = Settings()

    def get_embeddings(self, settings: Settings) -> AzureOpenAIEmbeddings:
        """Inizializza il modello di embedding Azure OpenAI.

        Args:
            settings: Configurazione corrente.

        Returns:
            AzureOpenAIEmbeddings: Oggetto embedding pronto all'uso.

        Raises:
            ValueError: Se le variabili d'ambiente richieste non sono impostate.
        """
        azure_endpoint = os.getenv("AZURE_API_BASE")
        azure_api_key = os.getenv("AZURE_API_KEY")
        azure_api_version = os.getenv("AZURE_API_VERSION")
        
        if not azure_endpoint:
            raise ValueError("AZURE_API_BASE environment variable is not set")
        if not azure_api_key:
            raise ValueError("AZURE_API_KEY environment variable is not set")
        if not azure_api_version:
            raise ValueError("AZURE_API_VERSION environment variable is not set")
        
        return AzureOpenAIEmbeddings(
            model="text-embedding-ada-002",
            azure_endpoint=azure_endpoint,
            api_key=azure_api_key,
            openai_api_version=azure_api_version
        )

    def get_llm(self, settings: Settings) -> AzureChatOpenAI:
        """Inizializza un modello chat su Azure OpenAI.

        Args:
            settings: Configurazione corrente.

        Returns:
            AzureChatOpenAI: Modello chat configurato.

        Raises:
            ValueError: Se le variabili d'ambiente richieste non sono impostate.
        """
        # Assicurati che le variabili d'ambiente siano caricate
        load_dotenv()
        
        azure_endpoint = os.getenv("AZURE_API_BASE")
        azure_api_key = os.getenv("AZURE_API_KEY")
        azure_api_version = os.getenv("AZURE_API_VERSION")
        
        if not azure_endpoint:
            raise ValueError("AZURE_API_BASE environment variable is not set")
        if not azure_api_key:
            raise ValueError("AZURE_API_KEY environment variable is not set")
        if not azure_api_version:
            raise ValueError("AZURE_API_VERSION environment variable is not set")
            
        return AzureChatOpenAI(
            azure_deployment="gpt-4o",
            azure_endpoint=azure_endpoint,
            api_key=azure_api_key,
            api_version=azure_api_version,
            temperature=0.1,
            max_tokens=None,
            timeout=None,
            max_retries=2,
        )

    def load_docs(self, path: str) -> List[Document]:
        """Carica un file di testo come elenco di documenti LangChain.

        Args:
            path: Percorso del file di testo.

        Returns:
            list[Document]: Un singolo documento con `page_content` e `metadata`.
        """
        doc = Path(path).read_text(encoding="utf-8")
        return [Document(page_content=doc, metadata={"source": path})]
    
    def split_documents(self, docs: List[Document], settings: Settings) -> List[Document]:
        """Esegue lo splitting dei documenti per ottimizzare il retrieval.

        Args:
            docs: Elenco di documenti di input.
            settings: Parametri di splitting (chunk size/overlap).

        Returns:
            list[Document]: Documenti suddivisi in chunk.
        """
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
            separators=["\n\n", "\n", ". ", "? ", "! ", "; ", ": ", ", ", " ", ""],
        )
        return splitter.split_documents(docs)


    # =========================
    # Qdrant: creazione collection + indici
    # =========================

    def get_qdrant_client(self, settings: Settings) -> QdrantClient:
        return QdrantClient(url=settings.qdrant_url)

    def recreate_collection_for_rag(self, client: QdrantClient, settings: Settings, vector_size: int):
        client.recreate_collection(
            collection_name=settings.collection,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
            hnsw_config=HnswConfigDiff(
                m=32,             # grado medio del grafo HNSW (maggiore = più memoria/qualità)
                ef_construct=256  # ampiezza lista candidati in fase costruzione (qualità/tempo build)
            ),
            optimizers_config=OptimizersConfigDiff(
                default_segment_number=2  # parallelismo/segmentazione iniziale
            ),
            quantization_config=ScalarQuantization(
                scalar=ScalarQuantizationConfig(type="int8", always_ram=False)  # on-disk quantization dei vettori
            ),
        )

        # Indice full-text sul campo 'text' per filtri MatchText
        client.create_payload_index(
            collection_name=settings.collection,
            field_name="text",
            field_schema=PayloadSchemaType.TEXT
        )

        # Indici keyword per filtri esatti / velocità nei filtri
        for key in ["doc_id", "source", "title", "lang"]:
            client.create_payload_index(
                collection_name=settings.collection,
                field_name=key,
                field_schema=PayloadSchemaType.KEYWORD
            )

    # =========================
    # Ingest: chunk -> embed -> upsert
    # =========================

    def build_points(self, chunks: List[Document], embeds: List[List[float]]) -> List[PointStruct]:
        pts: List[PointStruct] = []
        for i, (doc, vec) in enumerate(zip(chunks, embeds), start=1):
            payload = {
                "doc_id": doc.metadata.get("id"),
                "source": doc.metadata.get("source"),
                "title": doc.metadata.get("title"),
                "lang": doc.metadata.get("lang", "en"),
                "text": doc.page_content,
                "chunk_id": i - 1
            }
            pts.append(PointStruct(id=i, vector=vec, payload=payload))
        return pts

    def upsert_chunks(self, client: QdrantClient, settings: Settings, chunks: List[Document], embeddings: AzureOpenAIEmbeddings):
        vecs = embeddings.embed_documents([c.page_content for c in chunks])
        points = self.build_points(chunks, vecs)
        client.upsert(collection_name=settings.collection, points=points, wait=True)

    # =========================
    # Ricerca: semantica / testuale / ibrida
    # =========================

    def qdrant_semantic_search(
        self,
        client: QdrantClient,
        settings: Settings,
        query: str,
        embeddings: AzureOpenAIEmbeddings,
        limit: int,
        with_vectors: bool = False
    ):
        qv = embeddings.embed_query(query)
        res = client.query_points(
            collection_name=settings.collection,
            query=qv,
            limit=limit,
            with_payload=True,
            with_vectors=with_vectors,
            search_params=SearchParams(
                hnsw_ef=256,  # ampiezza lista in fase di ricerca (recall/latency)
                exact=False   # True = ricerca esatta (lenta); False = ANN HNSW
            ),
        )
        return res.points

    def qdrant_text_prefilter_ids(
        self,
        client: QdrantClient,
        settings: Settings,
        query: str,
        max_hits: int
    ) -> List[int]:
        # Scroll con filtro MatchText per ottenere id dei match testuali
        # (nota: scroll è paginato; qui prendiamo solo i primi max_hits per semplicità)
        matched_ids: List[int] = []
        next_page = None
        while True:
            points, next_page = client.scroll(
                collection_name=settings.collection,
                scroll_filter=Filter(
                    must=[FieldCondition(key="text", match=MatchText(text=query))]
                ),
                limit=min(256, max_hits - len(matched_ids)),
                offset=next_page,
                with_payload=False,
                with_vectors=False,
            )
            matched_ids.extend([p.id for p in points])
            if not next_page or len(matched_ids) >= max_hits:
                break
        return matched_ids

    def mmr_select(
        self,
        query_vec: List[float],
        candidates_vecs: List[List[float]],
        k: int,
        lambda_mult: float
    ) -> List[int]:

        import numpy as np
        V = np.array(candidates_vecs, dtype=float)
        q = np.array(query_vec, dtype=float)

        def cos(a, b):
            na = (a @ a) ** 0.5 + 1e-12
            nb = (b @ b) ** 0.5 + 1e-12
            return float((a @ b) / (na * nb))

        sims = [cos(v, q) for v in V]
        selected: List[int] = []
        remaining = set(range(len(V)))

        while len(selected) < min(k, len(V)):
            if not selected:
                # pick the highest similarity first
                best = max(remaining, key=lambda i: sims[i])
                selected.append(best)
                remaining.remove(best)
                continue
            best_idx = None
            best_score = -1e9
            for i in remaining:
                max_div = max([cos(V[i], V[j]) for j in selected]) if selected else 0.0
                score = lambda_mult * sims[i] - (1 - lambda_mult) * max_div
                if score > best_score:
                    best_score = score
                    best_idx = i
            selected.append(best_idx)
            remaining.remove(best_idx)
        return selected

    def hybrid_search(
        self,
        client: QdrantClient,
        settings: Settings,
        query: str,
        embeddings: AzureOpenAIEmbeddings
    ):
        # (1) semantica
        sem = self.qdrant_semantic_search(
            client, settings, query, embeddings,
            limit=settings.top_n_semantic, with_vectors=True
        )
        if not sem:
            return []

        # (2) full-text prefilter (id)
        text_ids = set(self.qdrant_text_prefilter_ids(client, settings, query, settings.top_n_text))

        # Normalizzazione score semantici per fusione
        scores = [p.score for p in sem]
        smin, smax = min(scores), max(scores)
        def norm(x):  # robusto al caso smin==smax
            return 1.0 if smax == smin else (x - smin) / (smax - smin)

        # (3) fusione con boost testuale
        fused: List[Tuple[int, float, Any]] = []  # (idx, fused_score, point)
        for idx, p in enumerate(sem):
            base = norm(p.score)                    # [0..1]
            fuse = settings.alpha * base
            if p.id in text_ids:
                fuse += settings.text_boost         # boost additivo
            fused.append((idx, fuse, p))

        # ordina per fused_score desc
        fused.sort(key=lambda t: t[1], reverse=True)

        # MMR opzionale per diversificare i top-K
        if settings.use_mmr:
            qv = embeddings.embed_query(query)
            # prendiamo i primi N dopo fusione (es. 30) e poi MMR per final_k
            N = min(len(fused), max(settings.final_k * 5, settings.final_k))
            cut = fused[:N]
            vecs = [sem[i].vector for i, _, _ in cut]
            mmr_idx = self.mmr_select(qv, vecs, settings.final_k, settings.mmr_lambda)
            picked = [cut[i][2] for i in mmr_idx]
            return picked

        # altrimenti, prendi i primi final_k dopo fusione
        return [p for _, _, p in fused[:settings.final_k]]

    # =========================
    # Prompt/Chain per generazione con citazioni
    # =========================

    def format_docs_for_prompt(self, points: Iterable[Any]) -> str:
        blocks = []
        for p in points:
            pay = p.payload or {}
            src = pay.get("source", "unknown")
            blocks.append(f"[source:{src}] {pay.get('text','')}")
        return "\n\n".join(blocks)

    def build_rag_chain(self, llm):
        system_prompt = (
            "Sei un assistente tecnico. Rispondi in italiano, conciso e accurato. "
            "Usa ESCLUSIVAMENTE le informazioni presenti nel CONTENUTO. "
            "Se non è presente, dichiara: 'Non è presente nel contesto fornito.' "
            "Cita sempre le fonti nel formato [source:FILE]."
        )

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human",
            "Domanda:\n{question}\n\n"
            "CONTENUTO:\n{context}\n\n"
            "Istruzioni:\n"
            "1) Risposta basata solo sul contenuto.\n"
            "2) Includi citazioni [source:...].\n"
            "3) Niente invenzioni.")
        ])

        chain = (
            {
                "context": RunnablePassthrough(),  # stringa già formattata
                "question": RunnablePassthrough(),
            }
            | prompt
            | llm
            | StrOutputParser()
        )
        return chain    




    
    
    def _run(self, query: str, run_manager=None) -> str:
        load_dotenv()

        embeddings = self.get_embeddings(self.SETTINGS)
        llm = self.get_llm(self.SETTINGS)

        # 1) Client Qdrant
        client = self.get_qdrant_client(self.SETTINGS)

        # 2) Dati -> chunk
        docs = self.load_docs('documents\\medicina_generale.txt')
        chunks = self.split_documents(docs, self.SETTINGS)

        # 3) Crea (o ricrea) collection
        vector_size = 1536  # dimensione embedding ada-002
        self.recreate_collection_for_rag(client, self.SETTINGS, vector_size)

        # 4) Upsert chunks
        self.upsert_chunks(client, self.SETTINGS, chunks, embeddings)

        hits = self.hybrid_search(client, self.SETTINGS, query, embeddings)
        print("=" * 80)
        print("Q:", query)
        if not hits:
            print("Nessun risultato.")

        # Mostra id/score di debug
        for p in hits:
            print(f"- id={p.id} score={p.score:.4f} src={p.payload.get('source')}")

        # Se LLM configurato: genera
        if llm:
            try:
                ctx = self.format_docs_for_prompt(hits)
                chain = self.build_rag_chain(llm)
                answer = chain.invoke({"question": query, "context": ctx})
                return answer
            except Exception as e:
                print(f"\nLLM generation failed: {e}")
        else:
            # Fallback: stampa i chunk per ispezione
            print("\nContenuto recuperato:\n")
            print(self.format_docs_for_prompt(hits))
            print()
