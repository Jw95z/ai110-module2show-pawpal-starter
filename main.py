from datetime import date

from pawpal_system import Owner, Pet, Task, Scheduler


def main() -> None:
    owner = Owner("Jordan")

    mochi = Pet(name="Mochi", species="dog", age=3)
    luna = Pet(name="Luna", species="cat", age=5)

    today = date.today()

    # Add tasks out of order on purpose
    mochi.add_task(Task("Breakfast", "08:30", "daily", today))
    mochi.add_task(Task("Morning walk", "07:30", "daily", today))
    luna.add_task(Task("Feed dinner", "18:00", "daily", today))
    luna.add_task(Task("Brush fur", "18:00", "weekly", today))
    mochi.add_task(Task("Medication", "18:00", "daily", today))

    owner.add_pet(mochi)
    owner.add_pet(luna)

    scheduler = Scheduler(owner)

    print("\nFULL SCHEDULE")
    print(scheduler.format_schedule(scheduler.sort_by_time(owner.get_all_tasks())))

    print("\nONLY MOCHI'S TASKS")
    mochi_tasks = scheduler.filter_tasks(pet_name="Mochi")
    print(scheduler.format_schedule(mochi_tasks))

    print("\nONLY PENDING TASKS")
    pending_tasks = scheduler.filter_tasks(completed=False)
    print(scheduler.format_schedule(pending_tasks))

    print("\nCONFLICT WARNINGS")
    warnings = scheduler.detect_conflicts()
    if warnings:
        for warning in warnings:
            print("-", warning)
    else:
        print("No conflicts detected.")

    print("\nMARKING MOCHI'S MORNING WALK COMPLETE...")
    scheduler.mark_task_complete("Mochi", "Morning walk", "07:30")

    print("\nTODAY'S PENDING SCHEDULE AFTER COMPLETION")
    print(scheduler.format_schedule(scheduler.get_todays_schedule(pending_only=True)))

    print("\nALL MOCHI TASKS AFTER RECURRING TASK RECREATION")
    mochi_tasks = scheduler.filter_tasks(pet_name="Mochi")
    print(scheduler.format_schedule(mochi_tasks))


if __name__ == "__main__":
    main()