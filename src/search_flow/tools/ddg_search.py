"""Strumento DuckDuckGo per ricerche testuali.

Espone `DDGSearch`, un tool compatibile con CrewAI per effettuare ricerche
testuali tramite DuckDuckGo e restituire risultati formattati.
"""

from typing import Any
from crewai.tools import BaseTool
from ddgs import DDGS

class DDGSearch(BaseTool):
    """Tool per eseguire ricerche su DuckDuckGo."""

    name: str = "duckduckgo_search"
    description: str = "Uno strumento per cercare risultati su DuckDuckGo"

    def _run(self, query: str, run_manager: Any | None = None) -> str:  # noqa: ARG002, W0613
        """Esegue una ricerca testuale su DuckDuckGo.

        Args:
            query: Testo della query da ricercare.

        Returns:
            str: Risultati formattati come elenco numerato con titolo, URL e snippet.

        Raises:
            ValueError: Se la query è vuota o None.
        """
        if not query:
            raise ValueError("Fornisci una query valida.")

        with DDGS(verify=False) as ddgs:
            risultati = list(ddgs.text(query, region="it-it", safesearch="off", max_results=3))

        output = []
        for i, r in enumerate(risultati, 1):
            titolo = r.get("title", "")
            url = r.get("href") or r.get("url") or ""
            snippet = r.get("body", "")
            output.append(f"{i}. {titolo}\n{url}\n{snippet}")

        return "\n\n".join(output)
