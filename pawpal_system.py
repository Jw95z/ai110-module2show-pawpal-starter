from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import List


@dataclass
class Task:
    """Represents a single pet care task."""

    description: str
    time: str
    frequency: str
    due_date: date
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.completed = True

    def mark_incomplete(self) -> None:
        """Mark the task as not completed."""
        self.completed = False

    def get_status(self) -> str:
        """Return the task's completion status."""
        return "Done" if self.completed else "Pending"

    def next_occurrence(self) -> Task | None:
        """Return a new task for the next recurring occurrence, if applicable."""
        if self.frequency.lower() == "daily":
            next_date = self.due_date + timedelta(days=1)
        elif self.frequency.lower() == "weekly":
            next_date = self.due_date + timedelta(weeks=1)
        else:
            return None

        return Task(
            description=self.description,
            time=self.time,
            frequency=self.frequency,
            due_date=next_date,
            completed=False,
        )


@dataclass
class Pet:
    """Stores pet details and the tasks assigned to that pet."""

    name: str
    species: str
    age: int = 0
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet."""
        self.tasks.append(task)

    def remove_task(self, description: str, time: str | None = None) -> bool:
        """Remove a matching task from this pet."""
        for i, task in enumerate(self.tasks):
            if task.description == description and (time is None or task.time == time):
                del self.tasks[i]
                return True
        return False

    def get_tasks(self) -> List[Task]:
        """Return all tasks for this pet."""
        return self.tasks

    def get_pending_tasks(self) -> List[Task]:
        """Return incomplete tasks for this pet."""
        return [task for task in self.tasks if not task.completed]


@dataclass
class Owner:
    """Stores owner details and manages that owner's pets."""

    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        self.pets.append(pet)

    def get_pets(self) -> List[Pet]:
        """Return all pets owned by this owner."""
        return self.pets

    def get_all_tasks(self) -> List[tuple[Pet, Task]]:
        """Return every task across all pets."""
        all_tasks: List[tuple[Pet, Task]] = []
        for pet in self.pets:
            for task in pet.tasks:
                all_tasks.append((pet, task))
        return all_tasks

    def get_all_pending_tasks(self) -> List[tuple[Pet, Task]]:
        """Return every incomplete task across all pets."""
        pending: List[tuple[Pet, Task]] = []
        for pet in self.pets:
            for task in pet.tasks:
                if not task.completed:
                    pending.append((pet, task))
        return pending


class Scheduler:
    """Retrieves, organizes, and manages pet care tasks."""

    def __init__(self, owner: Owner) -> None:
        """Initialize the scheduler with an owner."""
        self.owner = owner

    def _time_to_minutes(self, time_str: str) -> int:
        """Convert a HH:MM time string into total minutes."""
        hours, minutes = time_str.split(":")
        return int(hours) * 60 + int(minutes)

    def sort_by_time(self, tasks: List[tuple[Pet, Task]]) -> List[tuple[Pet, Task]]:
        """Return tasks sorted by due date and time."""
        return sorted(
            tasks,
            key=lambda item: (item[1].due_date, self._time_to_minutes(item[1].time))
        )

    def filter_tasks(
        self,
        pet_name: str | None = None,
        completed: bool | None = None,
    ) -> List[tuple[Pet, Task]]:
        """Filter tasks by pet name and/or completion status."""
        filtered = self.owner.get_all_tasks()

        if pet_name is not None:
            filtered = [
                (pet, task) for pet, task in filtered if pet.name.lower() == pet_name.lower()
            ]

        if completed is not None:
            filtered = [
                (pet, task) for pet, task in filtered if task.completed == completed
            ]

        return self.sort_by_time(filtered)

    def get_todays_schedule(self, pending_only: bool = False) -> List[tuple[Pet, Task]]:
        """Return today's tasks sorted by time."""
        today = date.today()

        tasks = self.owner.get_all_pending_tasks() if pending_only else self.owner.get_all_tasks()
        todays_tasks = [(pet, task) for pet, task in tasks if task.due_date == today]

        return self.sort_by_time(todays_tasks)

    def mark_task_complete(
        self,
        pet_name: str,
        description: str,
        time: str | None = None,
    ) -> bool:
        """Mark a task complete and auto-create the next recurring instance if needed."""
        for pet in self.owner.get_pets():
            if pet.name != pet_name:
                continue

            for task in pet.get_tasks():
                if task.description == description and (time is None or task.time == time):
                    task.mark_complete()

                    next_task = task.next_occurrence()
                    if next_task is not None:
                        pet.add_task(next_task)

                    return True

        return False

    def detect_conflicts(self, tasks: List[tuple[Pet, Task]] | None = None) -> List[str]:
        """Return warning messages for tasks scheduled at the same date and time."""
        if tasks is None:
            tasks = self.owner.get_all_tasks()

        warnings: List[str] = []
        grouped: dict[tuple[date, str], List[tuple[Pet, Task]]] = {}

        for pet, task in tasks:
            key = (task.due_date, task.time)
            grouped.setdefault(key, []).append((pet, task))

        for (due_date, time), entries in grouped.items():
            if len(entries) > 1:
                task_labels = [
                    f"{pet.name}: {task.description}"
                    for pet, task in entries
                ]
                warnings.append(
                    f"Conflict on {due_date.isoformat()} at {time} -> " + ", ".join(task_labels)
                )

        return warnings

    def format_schedule(self, tasks: List[tuple[Pet, Task]] | None = None) -> str:
        """Return a readable terminal version of a schedule."""
        if tasks is None:
            tasks = self.get_todays_schedule()

        if not tasks:
            return "Today's Schedule\n-----------------\nNo tasks scheduled."

        lines = ["Today's Schedule", "-----------------"]
        for pet, task in tasks:
            lines.append(
                f"{task.due_date.isoformat()} {task.time} | "
                f"{pet.name} ({pet.species}) | "
                f"{task.description} [{task.frequency}] - {task.get_status()}"
            )

        return "\n".join(lines)