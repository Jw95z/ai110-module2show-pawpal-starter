from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class Owner:
    name: str
    available_minutes_per_day: int
    preferences: Dict[str, str] = field(default_factory=dict)

    def update_preferences(self, preferences: Dict[str, str]) -> None:
        """Update owner preferences."""
        pass

    def set_available_time(self, minutes: int) -> None:
        """Set how much time the owner has for pet care in a day."""
        pass


@dataclass
class Pet:
    name: str
    species: str
    age: int = 0
    notes: str = ""

    def add_note(self, note: str) -> None:
        """Add a care note or reminder for this pet."""
        pass

    def get_summary(self) -> str:
        """Return a short summary of the pet."""
        pass


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str
    category: str = "general"
    required: bool = False
    pet_name: str = ""

    def is_high_priority(self) -> bool:
        """Return True if the task is high priority."""
        pass

    def describe(self) -> str:
        """Return a readable description of the task."""
        pass


@dataclass
class ScheduleItem:
    task: Task
    start_minute: int
    end_minute: int
    reason: str = ""

    def describe(self) -> str:
        """Return a readable description of this scheduled item."""
        pass


class Scheduler:
    def __init__(self, owner: Owner, pet: Pet) -> None:
        self.owner = owner
        self.pet = pet
        self.tasks: List[Task] = []

    def add_task(self, task: Task) -> None:
        """Add a task to the scheduler."""
        pass

    def remove_task(self, task_title: str) -> None:
        """Remove a task by title."""
        pass

    def sort_tasks(self) -> List[Task]:
        """Return tasks sorted by priority and other scheduling rules."""
        pass

    def generate_daily_plan(self) -> List[ScheduleItem]:
        """Generate a daily plan based on available time and task priority."""
        pass

    def explain_plan(self, plan: List[ScheduleItem]) -> List[str]:
        """Explain why each task was selected and scheduled."""
        pass