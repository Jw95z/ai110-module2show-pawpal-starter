from datetime import date, timedelta

from pawpal_system import Owner, Pet, Task, Scheduler


def test_mark_complete_changes_task_status() -> None:
    task = Task(description="Morning walk", time="08:00", frequency="daily", due_date=date.today())

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_pet_task_count() -> None:
    pet = Pet(name="Mochi", species="dog")
    initial_count = len(pet.tasks)

    pet.add_task(Task(description="Breakfast", time="08:30", frequency="daily", due_date=date.today()))

    assert len(pet.tasks) == initial_count + 1


def test_scheduler_sorts_tasks_in_chronological_order() -> None:
    owner = Owner("Jordan")
    pet = Pet("Mochi", "dog")
    today = date.today()

    pet.add_task(Task("Late task", "10:00", "daily", today))
    pet.add_task(Task("Early task", "07:30", "daily", today))
    pet.add_task(Task("Middle task", "08:45", "daily", today))

    owner.add_pet(pet)
    scheduler = Scheduler(owner)

    schedule = scheduler.get_todays_schedule()

    descriptions = [task.description for _, task in schedule]
    assert descriptions == ["Early task", "Middle task", "Late task"]


def test_daily_task_completion_creates_next_occurrence() -> None:
    owner = Owner("Jordan")
    pet = Pet("Mochi", "dog")
    today = date.today()

    pet.add_task(Task("Morning walk", "08:00", "daily", today))
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    result = scheduler.mark_task_complete("Mochi", "Morning walk", "08:00")

    assert result is True
    assert len(pet.tasks) == 2
    assert pet.tasks[0].completed is True
    assert pet.tasks[1].description == "Morning walk"
    assert pet.tasks[1].due_date == today + timedelta(days=1)
    assert pet.tasks[1].completed is False


def test_conflict_detection_flags_duplicate_times() -> None:
    owner = Owner("Jordan")
    dog = Pet("Mochi", "dog")
    cat = Pet("Luna", "cat")
    today = date.today()

    dog.add_task(Task("Morning walk", "08:00", "daily", today))
    cat.add_task(Task("Breakfast", "08:00", "daily", today))

    owner.add_pet(dog)
    owner.add_pet(cat)

    scheduler = Scheduler(owner)
    warnings = scheduler.detect_conflicts()

    assert len(warnings) == 1
    assert "08:00" in warnings[0]


def test_pet_with_no_tasks_returns_empty_schedule() -> None:
    owner = Owner("Jordan")
    pet = Pet("Mochi", "dog")
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    schedule = scheduler.get_todays_schedule()

    assert schedule == []


def test_filter_by_pet_name_returns_only_matching_pet_tasks() -> None:
    owner = Owner("Jordan")
    dog = Pet("Mochi", "dog")
    cat = Pet("Luna", "cat")
    today = date.today()

    dog.add_task(Task("Walk", "08:00", "daily", today))
    cat.add_task(Task("Feed", "09:00", "daily", today))

    owner.add_pet(dog)
    owner.add_pet(cat)

    scheduler = Scheduler(owner)
    filtered = scheduler.filter_tasks(pet_name="Mochi")

    assert len(filtered) == 1
    assert filtered[0][0].name == "Mochi"
    assert filtered[0][1].description == "Walk"