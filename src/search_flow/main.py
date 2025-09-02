"""Entry point e definizioni del flow di ricerca.

Questo modulo definisce lo stato `SearchState` e il flow `SearchFlow` che
smista le richieste tra ricerca documentale (RAG) e ricerca web, più utility
per avviare o plottare il diagramma del flow.
"""

from pydantic import BaseModel
from dotenv import load_dotenv
from crewai.flow.flow import Flow, start, listen, router
from crewai import LLM
from search_flow.crews.search_crew.search_crew import SearchCrew
from search_flow.crews.rag_crew.rag_crew import RAGCrew

load_dotenv()

class SearchState(BaseModel):
    """Stato condiviso del flow di ricerca.

    Attributes:
        question: Domanda dell'utente.
        type: Tipo di richiesta rilevato ("medicina" o "altro").
        result: Risultato della ricerca documentale.
        raw_results: Risultati grezzi ottenuti dalla ricerca web.
        summary: Riassunto dei risultati della ricerca web.
    """

    question: str = ""
    type: str = ""
    result: str = ""
    raw_results: str = ""
    summary: str = ""

class SearchFlow(Flow[SearchState]):
    """Flow di orchestrazione tra RAG e ricerca web."""

    rag_crew = RAGCrew()
    search_crew = SearchCrew()

    @start()
    def detect_field(self):
        """Determina se l'intento dell'utente è medico o generico.

        Returns:
            SearchState: Stato aggiornato con `question` e `type`.
        """

        self.state.question = input("Chiedimi quello che vuoi!\n> ")

        llm = LLM(model="azure/gpt-4o-mini")
        messages = [
            {
                "role": "system",
                "content": (
                    "Sei un assistente che capisce se l'utente ti sta facendo una domanda "
                    "relativa al campo della medicina, oppure qualche altro campo. Se è relativo "
                    "alla medicina, rispondi solo 'medicina', altrimenti rispondi solo 'altro'."
                ),
            },
            {"role": "user", "content": self.state.question},
        ]

        self.state.type = llm.call(messages)
        return self.state

    @router(detect_field)
    def route_field(self):
        """Smista il flow in base all'intento rilevato.

        Returns:
            str | None: La route "medicina" o "altro"; None se non determinabile.
        """
        if self.state.type.lower() == "medicina":
            return 'medicina'
        if self.state.type.lower() == "altro":
            return 'altro'
        print("\n⚠️ Non ho capito cosa vuoi fare.")
        return None

    @listen('medicina')
    def rag(self):
        """Esegue la ricerca RAG sui documenti locali.

        Returns:
            SearchState: Stato con `result` aggiornato.
        """

        document_searcher = self.rag_crew.document_searcher()
        self.state.result = document_searcher.execute_task(
            task=self.rag_crew.document_search_task(),
            context=self.state.question
        )

        print(self.state.result)

        return self.state

    @listen('altro')
    def run_research(self):
        """Esegue la ricerca web tramite DuckDuckGo.

        Returns:
            SearchState: Stato con `raw_results` aggiornato.
        """
        researcher = self.search_crew.researcher()
        self.state.raw_results = researcher.execute_task(
            task=self.search_crew.research_task(),
            context=self.state.question
        )
        print("\n=== RISULTATI GREZZI DAL WEB ===\n", self.state.raw_results)
        return self.state

    @listen(run_research)
    def run_summary(self):
        """Riassume i risultati della ricerca web.

        Returns:
            SearchState: Stato con `summary` aggiornato.
        """
        resumer = self.search_crew.resumer()
        self.state.summary = resumer.execute_task(
            task=self.search_crew.resume_task(),
            context=self.state.raw_results
        )
        print("\n=== RIASSUNTO ===\n", self.state.summary)
        return self.state

def kickoff():
    """Avvia l'esecuzione interattiva del flow di ricerca."""
    f = SearchFlow()
    f.kickoff()

def plot():
    """Genera il diagramma del flow in `search_flow_diagram.html`."""
    f = SearchFlow()
    f.plot("search_flow_diagram")

if __name__ == "__main__":
    kickoff()
