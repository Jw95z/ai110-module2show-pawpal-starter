from pawpal_system import Task, Pet


def test_mark_complete_changes_task_status() -> None:
    task = Task(description="Morning walk", time="08:00", frequency="daily")

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_pet_task_count() -> None:
    pet = Pet(name="Mochi", species="dog")
    initial_count = len(pet.tasks)

    pet.add_task(Task(description="Breakfast", time="08:30", frequency="daily"))

    assert len(pet.tasks) == initial_count + 1