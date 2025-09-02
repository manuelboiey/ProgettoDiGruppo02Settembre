==============================
Data Compliance
==============================

Overview
========
This project’s retrieval-augmented generation (RAG) uses a **single, local, Italian-language text file** on general medicine as its knowledge source. The assistant is instructed to answer **exclusively** from the retrieved context and to include inline citations in the form ``[source:FILE]``.

- Local source file: ``documents\medicina_generale.txt`` (loaded directly by the RAG tool).
- The content is an expository primer on *medicina generale* (general practice/family medicine), with sections such as history, role of the GP, prevention, patient–doctor relationship, SSN integration, chronic disease management, and telemedicine. It contains **no personal data** and no labels.

Known Usage in the System
=========================
- When the routing detects a *medical* intent, the pipeline runs the **RAG** document search over the local knowledge and returns a cited answer. For *non-medical* intent, it performs a web search and summary (DuckDuckGo).

Dataset Characteristics
=======================
- **Type:** Unstructured text (Italian) on general medicine.
- **Instances/Files:** Single file (loaded as one LangChain ``Document`` and then chunked).
- **Labels/Targets:** None (knowledge-only, used for retrieval/grounding).
- **Personal or special-category data:** None observed in the source text.
- **Primary use:** Local knowledge base for RAG answers to medicine-related questions (answers restricted to retrieved context and cited).

Origin and Provenance
=====================
- **Source:** Internally authored synthetic text (generated with ChatGPT, per team note) and stored locally as ``documents\medicina_generale.txt``. (Team statement)
- **Third-party data:** Not used (no external datasets referenced in code for the medical knowledge path). Loading is from local filesystem.
- **Geographic/temporal scope:** General informational content; not tied to individuals or time-stamped records.

Pre-processing and Indexing
===========================
- **Loading:** Read as UTF-8 and wrapped into a single LangChain ``Document`` with ``metadata['source'] = path``.
- **Chunking:** Recursive splitting with **chunk_size = 1500** and **chunk_overlap = 300** (see ``Settings``), to optimize retrieval.
- **Vector store:** FAISS index persisted under the ``faiss/`` directory; if present, it is reloaded on startup.
- **Retrieval:** Configurable **MMR** (default) or similarity search; typical kwargs include ``k``, ``fetch_k``, and ``lambda_mult``.
- **Prompting constraints:** The system prompt mandates: answer in Italian; **use only the provided context**; **always include citations** in ``[source:...]`` format; state when information is not in context.

Access, Retention, and Distribution
===================================
- **Access path:** Local file system (``documents\medicina_generale.txt``). No remote fetching for the medical knowledge path.
- **Derived artefacts:** FAISS index files (``index.faiss``, ``index.pkl``) persisted in ``faiss/``.
- **Distribution/licensing:** Internal project asset; not redistributed by the codebase.

Bias, Fairness, and Safety Notes
================================
- **Team review:** You report that a manual review found **no bias or discriminatory content** in the dataset (neutral, educational tone). The RAG chain further constrains outputs to the dataset content and requires explicit citations, which reduces the risk of unsupported or harmful claims. (Team statement)

Deployer Guidance (Responsible Use)
===================================
- Answers must remain within the retrieved context; if something is **not** in the text, the assistant should state that explicitly. Keep the medical scope to general information—**no personal advice**, diagnoses, or treatment decisions are contained in the dataset.

Appendix: File Pointers
=======================
- Knowledge file: ``documents\medicina_generale.txt`` (loaded in RAG tool).
- RAG tool (loading/chunking/retrieval/prompting/citations): ``search_flow/tools/rag.py``.
- Flow routing (medical vs other): ``main.py`` (SearchFlow).
- Web search path (non-medical): ``search_flow/tools/ddg_search.py`` and ``search_flow/crews/search_crew.py``.
