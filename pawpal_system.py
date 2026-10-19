"""PawPal+ logic layer: the backend classes for the pet care planner.

Phase 1 skeleton: classes and attributes match diagrams/uml.mmd.
Method bodies are stubs and will be implemented in Phase 2.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Task:
    """One pet care activity, like a walk, feeding, or medication."""

    title: str
    duration_minutes: int
    priority: str = "medium"  # "low", "medium", or "high"
    time: Optional[str] = None  # preferred time, e.g. "08:00"
    frequency: str = "daily"  # "daily" or "weekly"
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as done."""
        pass

    def edit(self, duration_minutes: int, priority: str) -> None:
        """Change how long this task takes and how important it is."""
        pass


@dataclass
class Pet:
    """A pet and the care tasks it needs."""

    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a care task for this pet."""
        pass

    def remove_task(self, task: Task) -> None:
        """Remove a care task from this pet."""
        pass

    def get_tasks(self) -> List[Task]:
        """Return all of this pet's tasks."""
        pass


class Owner:
    """The person using PawPal+, who owns one or more pets."""

    def __init__(self, name: str, available_minutes: int, preferences: Optional[List[str]] = None):
        self.name = name
        self.available_minutes = available_minutes
        self.preferences = preferences or []
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        pass

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from this owner."""
        pass

    def get_pets(self) -> List[Pet]:
        """Return all of this owner's pets."""
        pass


class Scheduler:
    """Builds a daily care plan from the owner's pets and tasks."""

    def __init__(self, owner: Owner):
        self.owner = owner
        self.planned_tasks: List[Task] = []  # tasks chosen for today
        self.skipped_tasks: List[Task] = []  # tasks that didn't fit, so explain_plan can say why

    def generate_plan(self) -> List[Task]:
        """Pick the tasks that fit in the owner's available time today."""
        pass

    def sort_by_priority(self, tasks: List[Task]) -> List[Task]:
        """Return tasks ordered so high-priority tasks come first."""
        pass

    def explain_plan(self) -> str:
        """Explain why each task was included or skipped."""
        pass
