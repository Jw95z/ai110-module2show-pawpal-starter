from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    """Represents a single pet care task."""

    description: str
    time: str
    frequency: str
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.completed = True

    def mark_incomplete(self) -> None:
        """Mark the task as not completed."""
        self.completed = False

    def get_status(self) -> str:
        """Return the task's completion status as text."""
        return "Done" if self.completed else "Pending"


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
        """Remove a task by description and optional time."""
        for i, task in enumerate(self.tasks):
            if task.description == description and (time is None or task.time == time):
                del self.tasks[i]
                return True
        return False

    def get_tasks(self) -> List[Task]:
        """Return all tasks for this pet."""
        return self.tasks

    def get_pending_tasks(self) -> List[Task]:
        """Return only incomplete tasks for this pet."""
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
            for task in pet.get_tasks():
                all_tasks.append((pet, task))
        return all_tasks

    def get_all_pending_tasks(self) -> List[tuple[Pet, Task]]:
        """Return every incomplete task across all pets."""
        pending_tasks: List[tuple[Pet, Task]] = []
        for pet in self.pets:
            for task in pet.get_pending_tasks():
                pending_tasks.append((pet, task))
        return pending_tasks


class Scheduler:
    """Retrieves, organizes, and manages pet care tasks."""

    def __init__(self, owner: Owner) -> None:
        """Initialize the scheduler with an owner."""
        self.owner = owner

    def get_todays_schedule(self, pending_only: bool = False) -> List[tuple[Pet, Task]]:
        """Return all tasks sorted by time."""
        tasks = (
            self.owner.get_all_pending_tasks()
            if pending_only
            else self.owner.get_all_tasks()
        )
        return sorted(tasks, key=lambda item: self._time_to_minutes(item[1].time))

    def mark_task_complete(self, pet_name: str, description: str, time: str | None = None) -> bool:
        """Mark a matching task as complete."""
        for pet in self.owner.get_pets():
            if pet.name == pet_name:
                for task in pet.get_tasks():
                    if task.description == description and (time is None or task.time == time):
                        task.mark_complete()
                        return True
        return False

    def _time_to_minutes(self, time_str: str) -> int:
        """Convert a HH:MM time string into total minutes."""
        hours, minutes = time_str.split(":")
        return int(hours) * 60 + int(minutes)

    def format_schedule(self, pending_only: bool = False) -> str:
        """Return a readable terminal version of the schedule."""
        schedule = self.get_todays_schedule(pending_only=pending_only)

        if not schedule:
            return "Today's Schedule\n-----------------\nNo tasks scheduled."

        lines = ["Today's Schedule", "-----------------"]
        for pet, task in schedule:
            lines.append(
                f"{task.time} | {pet.name} ({pet.species}) | "
                f"{task.description} [{task.frequency}] - {task.get_status()}"
            )
        return "\n".join(lines)