"""Crew di ricerca web basata su DuckDuckGo.

Questo modulo definisce la `SearchCrew`, che collega agenti e task per
ricerca sul web e successivo riassunto dei risultati.
"""

from typing import Any, Dict, cast
from crewai import Agent, Crew, Task
from crewai.project import CrewBase, agent, crew, task
from search_flow.tools.ddg_search import DDGSearch
from search_flow.crews.utils import build_sequential_crew

@CrewBase
class SearchCrew:
    """Crew per ricerca e sintesi di informazioni dal web.

    Attributes:
        agents_config: Percorso al file YAML di configurazione degli agenti.
        tasks_config: Percorso al file YAML di configurazione dei task.
    """
    agents_config: Any = "config/agents.yaml"
    tasks_config: Any = "config/tasks.yaml"
    agents: Any
    tasks: Any

    # ------ Agents ------
    @agent
    def researcher(self) -> Agent:
        """Crea l'agente responsabile della ricerca web.

        Returns:
            Agent: Agente configurato con lo strumento `DDGSearch`.
        """
        # "agents_config" è popolato dinamicamente dal framework CrewAI (dict-like)
        # type: ignore[assignment]
        config_dict: Dict[str, Any] = cast(Dict[str, Any], self.agents_config)  # noqa: E1101
        return Agent(
            config=config_dict.get("researcher"),
            verbose=True,
            tools=[DDGSearch()],
        )
    @agent
    def resumer(self) -> Agent:
        """Crea l'agente che riassume i risultati della ricerca.

        Returns:
            Agent: Agente di riassunto configurato.
        """
        # type: ignore[assignment]
        config_dict: Dict[str, Any] = cast(Dict[str, Any], self.agents_config)  # noqa: E1101
        return Agent(
            config=config_dict.get("resumer"),
            verbose=True,
        )

    
    # ------ Tasks ------
    @task
    def research_task(self) -> Task:
        """Restituisce il task di ricerca web.

        Returns:
            Task: Task caricato dalla configurazione.
        """
        # type: ignore[assignment]
        tasks_dict: Dict[str, Any] = cast(Dict[str, Any], self.tasks_config)  # noqa: E1101
        return Task(config=tasks_dict.get("research_task"))

    @task
    def resume_task(self) -> Task:
        """Restituisce il task di riassunto dei risultati.

        Returns:
            Task: Task caricato dalla configurazione.
        """
        # type: ignore[assignment]
        tasks_dict: Dict[str, Any] = cast(Dict[str, Any], self.tasks_config)  # noqa: E1101
        return Task(config=tasks_dict.get("resume_task"))


    # ------ Crew ------
    @crew
    def crew(self) -> Crew:
        """Assembla e restituisce la crew di ricerca web.

        Returns:
            Crew: Crew con agenti e task eseguiti in sequenza.
        """
        return build_sequential_crew(self.agents, self.tasks, verbose=True)
