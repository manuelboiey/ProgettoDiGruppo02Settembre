"""RAG crew definitions for document retrieval tasks.

This module exposes the `RAGCrew`, which wires up agents and tasks to perform
retrieval-augmented generation over local documents using the `RAG` tool.
"""

from typing import Any, Dict, cast
from crewai import Agent, Crew, Task
from crewai.project import CrewBase, agent, crew, task
from search_flow.tools.rag import RAG
from search_flow.crews.utils import build_sequential_crew

@CrewBase
class RAGCrew:
    """Crew that performs document search over local knowledge.

    Attributes:
        agents_config: Path to the YAML configuration for agents.
        tasks_config: Path to the YAML configuration for tasks.
    """
    agents_config: Any = "config/agents.yaml"
    tasks_config: Any = "config/tasks.yaml"

    # ------ Agents ------
    @agent
    def document_searcher(self) -> Agent:
        """Create the agent responsible for document search.

        Returns:
            Agent: Configured agent with the `RAG` tool attached.
        """
        # type: ignore[assignment]
        config_dict: Dict[str, Any] = cast(Dict[str, Any], self.agents_config)  # noqa: E1101
        return Agent(
            config=config_dict.get("document_searcher"),
            verbose=True,
            tools=[RAG()]  # Usa lo strumento RAG definito in src/search_flow/tools/rag.py
        )

    # ------ Tasks ------
    @task
    def document_search_task(self) -> Task:
        """Return the task configuration for document search.

        Returns:
            Task: Task loaded from the tasks configuration.
        """
        # type: ignore[assignment]
        tasks_dict: Dict[str, Any] = cast(Dict[str, Any], self.tasks_config)  # noqa: E1101
        return Task(config=tasks_dict.get("document_search_task"))


    # ------ Crew ------
    @crew
    def crew(self) -> Crew:
        """Assemble and return the crew that executes the pipeline.

        Returns:
            Crew: Crew with agents and tasks in sequential process.
        """
        return build_sequential_crew(self.agents, self.tasks, verbose=True)
