"""Utility helpers for crew construction and common patterns."""

from typing import Any
from crewai import Crew, Process


def build_sequential_crew(agents: Any, tasks: Any, verbose: bool = True) -> Crew:
    """Create a sequential `Crew` with the provided agents and tasks.

    Args:
        agents: Elenco di agenti CrewAI.
        tasks: Elenco di task CrewAI.
        verbose: Abilita log verbosi.

    Returns:
        Crew: Crew configurata in modalità sequenziale.
    """
    return Crew(
        agents=agents,
        tasks=tasks,
        process=Process.sequential,
        verbose=verbose,
    )
