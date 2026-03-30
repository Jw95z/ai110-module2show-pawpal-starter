from datetime import date, timedelta

from pawpal_system import Owner, Pet, Task, Scheduler


def test_scheduler_sorts_tasks_by_time() -> None:
    owner = Owner("Jordan")
    pet = Pet("Mochi", "dog")
    today = date.today()

    pet.add_task(Task("Late task", "10:00", "daily", today))
    pet.add_task(Task("Early task", "08:00", "daily", today))
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    tasks = scheduler.get_todays_schedule()

    assert tasks[0][1].description == "Early task"
    assert tasks[1][1].description == "Late task"


def test_filter_tasks_by_pet_name() -> None:
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


def test_daily_task_creates_next_occurrence_when_completed() -> None:
    owner = Owner("Jordan")
    pet = Pet("Mochi", "dog")
    today = date.today()

    pet.add_task(Task("Walk", "08:00", "daily", today))
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    scheduler.mark_task_complete("Mochi", "Walk", "08:00")

    assert len(pet.tasks) == 2
    assert pet.tasks[0].completed is True
    assert pet.tasks[1].due_date == today + timedelta(days=1)
    assert pet.tasks[1].completed is False


def test_conflict_detection_finds_exact_time_match() -> None:
    owner = Owner("Jordan")
    dog = Pet("Mochi", "dog")
    cat = Pet("Luna", "cat")
    today = date.today()

    dog.add_task(Task("Walk", "08:00", "daily", today))
    cat.add_task(Task("Feed", "08:00", "daily", today))

    owner.add_pet(dog)
    owner.add_pet(cat)

    scheduler = Scheduler(owner)
    warnings = scheduler.detect_conflicts()

    assert len(warnings) == 1
    assert "08:00" in warnings[0]