"""PawPal+ logic layer: the backend classes for the pet care planner.

Classes and attributes match diagrams/uml.mmd.
"""

from dataclasses import dataclass, field, replace
from datetime import date, timedelta
from typing import List, Optional

# Lower number = more important, so sorting puts "high" first.
PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}

# How far ahead the next copy of a recurring task is due.
RECURRENCE_GAP = {"daily": timedelta(days=1), "weekly": timedelta(weeks=1)}


@dataclass
class Task:
    """One pet care activity, like a walk, feeding, or medication."""

    title: str
    duration_minutes: int
    priority: str = "medium"  # "low", "medium", or "high"
    time: Optional[str] = None  # preferred time, e.g. "08:00"
    frequency: str = "daily"  # "daily" or "weekly"
    completed: bool = False
    pet_name: Optional[str] = None  # set by Pet.add_task so the plan can show whose task it is
    due_date: date = field(default_factory=date.today)

    def mark_complete(self) -> Optional["Task"]:
        """Mark this task as done and return the next occurrence if it repeats."""
        self.completed = True
        gap = RECURRENCE_GAP.get(self.frequency)
        if gap is None:
            return None
        return replace(self, completed=False, due_date=self.due_date + gap)

    def edit(self, duration_minutes: int, priority: str) -> None:
        """Change how long this task takes and how important it is."""
        if priority not in PRIORITY_ORDER:
            raise ValueError(f"priority must be one of {list(PRIORITY_ORDER)}")
        self.duration_minutes = duration_minutes
        self.priority = priority


@dataclass
class Pet:
    """A pet and the care tasks it needs."""

    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a care task for this pet."""
        task.pet_name = self.name
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a care task from this pet."""
        if task in self.tasks:
            self.tasks.remove(task)

    def get_tasks(self) -> List[Task]:
        """Return all of this pet's tasks."""
        return self.tasks


class Owner:
    """The person using PawPal+, who owns one or more pets."""

    def __init__(self, name: str, available_minutes: int, preferences: Optional[List[str]] = None):
        self.name = name
        self.available_minutes = available_minutes
        self.preferences = preferences or []
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from this owner."""
        if pet in self.pets:
            self.pets.remove(pet)

    def get_pets(self) -> List[Pet]:
        """Return all of this owner's pets."""
        return self.pets

    def get_all_tasks(self) -> List[Task]:
        """Return every task from every pet in one list."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


class Scheduler:
    """Builds a daily care plan from the owner's pets and tasks."""

    def __init__(self, owner: Owner):
        self.owner = owner
        self.planned_tasks: List[Task] = []  # tasks chosen for today
        self.skipped_tasks: List[Task] = []  # tasks that didn't fit, so explain_plan can say why

    def generate_plan(self) -> List[Task]:
        """Pick the tasks that fit in the owner's available time today."""
        self.planned_tasks = []
        self.skipped_tasks = []

        # Read from the Owner so tasks from every pet are included.
        # Future copies of recurring tasks (due after today) are left out.
        today = date.today()
        pending = [
            task for task in self.owner.get_all_tasks() if not task.completed and task.due_date <= today
        ]

        minutes_left = self.owner.available_minutes
        for task in self.sort_by_priority(pending):
            if task.duration_minutes <= minutes_left:
                self.planned_tasks.append(task)
                minutes_left -= task.duration_minutes
            else:
                self.skipped_tasks.append(task)

        return self.planned_tasks

    def sort_by_priority(self, tasks: List[Task]) -> List[Task]:
        """Return tasks ordered so high-priority tasks come first."""
        # Ties are broken by preferred time; tasks with no time go last.
        return sorted(
            tasks,
            key=lambda task: (PRIORITY_ORDER.get(task.priority, len(PRIORITY_ORDER)), task.time or "99:99"),
        )

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Return tasks in clock order ("07:30" before "08:00"); tasks with no time go last."""
        # Zero-padded "HH:MM" strings sort correctly as text, so no time parsing is needed.
        return sorted(tasks, key=lambda task: task.time or "99:99")

    def mark_task_complete(self, task: Task) -> Optional[Task]:
        """Complete a task and, if it repeats, add its next occurrence to the same pet."""
        next_task = task.mark_complete()
        if next_task is not None:
            for pet in self.owner.get_pets():
                if pet.name == task.pet_name:
                    pet.add_task(next_task)
                    break
        return next_task

    def filter_tasks(self, pet_name: Optional[str] = None, completed: Optional[bool] = None) -> List[Task]:
        """Return the owner's tasks, optionally only for one pet and/or one completion status."""
        tasks = self.owner.get_all_tasks()
        if pet_name is not None:
            tasks = [task for task in tasks if task.pet_name == pet_name]
        if completed is not None:
            tasks = [task for task in tasks if task.completed == completed]
        return tasks

    def detect_conflicts(self) -> List[str]:
        """Return a warning for each time slot that has more than one task (exact time match only)."""
        today = date.today()
        by_time = {}
        for task in self.owner.get_all_tasks():
            if task.time and not task.completed and task.due_date <= today:
                by_time.setdefault(task.time, []).append(task)

        warnings = []
        for time, tasks in sorted(by_time.items()):
            if len(tasks) > 1:
                names = ", ".join(f"'{task.title}' ({task.pet_name})" for task in tasks)
                warnings.append(f"Conflict at {time}: {names} are scheduled at the same time.")
        return warnings

    def explain_plan(self) -> str:
        """Explain why each task was included or skipped."""
        if not self.planned_tasks and not self.skipped_tasks:
            return "No plan yet. Add some tasks and call generate_plan() first."

        lines = [f"{self.owner.name} has {self.owner.available_minutes} minutes today."]
        used = 0
        for task in self.planned_tasks:
            used += task.duration_minutes
            lines.append(
                f"Included '{task.title}' for {task.pet_name}: {task.priority} priority, "
                f"{task.duration_minutes} min (total so far {used} min)."
            )
        for task in self.skipped_tasks:
            lines.append(
                f"Skipped '{task.title}' for {task.pet_name}: needs {task.duration_minutes} min "
                f"but not enough time was left after higher-priority tasks."
            )
        return "\n".join(lines)
