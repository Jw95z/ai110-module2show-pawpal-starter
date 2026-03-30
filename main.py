from pawpal_system import Owner, Pet, Task, Scheduler


def main() -> None:
    owner = Owner("Jordan")

    dog = Pet(name="Mochi", species="dog", age=3)
    cat = Pet(name="Luna", species="cat", age=5)

    dog.add_task(Task(description="Morning walk", time="08:00", frequency="daily"))
    dog.add_task(Task(description="Breakfast", time="08:30", frequency="daily"))
    cat.add_task(Task(description="Feed dinner", time="18:00", frequency="daily"))
    cat.add_task(Task(description="Brush fur", time="19:00", frequency="weekly"))

    owner.add_pet(dog)
    owner.add_pet(cat)

    scheduler = Scheduler(owner)

    print(scheduler.format_schedule())

    print("\nMarking Mochi's Morning walk as complete...\n")
    scheduler.mark_task_complete("Mochi", "Morning walk", "08:00")

    print(scheduler.format_schedule())


if __name__ == "__main__":
    main()