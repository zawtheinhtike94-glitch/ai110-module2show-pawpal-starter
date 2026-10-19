"""Demo script: builds a sample owner, pets, and tasks, then prints today's schedule."""

from pawpal_system import Owner, Pet, Scheduler, Task


def print_schedule(scheduler: Scheduler) -> None:
    """Print the generated plan as a readable table, followed by the reasoning."""
    owner = scheduler.owner
    plan = scheduler.generate_plan()

    print("=" * 56)
    print(f"  Today's Schedule for {owner.name} ({owner.available_minutes} min available)")
    print("=" * 56)
    print(f"  {'Time':<7}{'Task':<18}{'Pet':<10}{'Min':>4}  Priority")
    print("  " + "-" * 52)
    for task in plan:
        time = task.time or "any"
        print(f"  {time:<7}{task.title:<18}{task.pet_name:<10}{task.duration_minutes:>4}  {task.priority}")

    used = sum(task.duration_minutes for task in plan)
    print("  " + "-" * 52)
    print(f"  Total: {used} of {owner.available_minutes} min")

    if scheduler.skipped_tasks:
        print("\n  Skipped (not enough time):")
        for task in scheduler.skipped_tasks:
            print(f"    - {task.title} for {task.pet_name} ({task.duration_minutes} min, {task.priority})")

    print("\nWhy this plan:")
    print(scheduler.explain_plan())


def main() -> None:
    owner = Owner("Jordan", available_minutes=90, preferences=["walks in the morning"])

    biscuit = Pet("Biscuit", "dog", 3)
    mochi = Pet("Mochi", "cat", 5)
    owner.add_pet(biscuit)
    owner.add_pet(mochi)

    biscuit.add_task(Task("Morning walk", 30, "high", time="07:30"))
    biscuit.add_task(Task("Breakfast", 10, "high", time="08:00"))
    biscuit.add_task(Task("Bath", 45, "low", time="17:00", frequency="weekly"))
    mochi.add_task(Task("Feeding", 10, "high", time="08:15"))
    mochi.add_task(Task("Medication", 5, "medium", time="09:00"))
    mochi.add_task(Task("Play session", 20, "medium", time="18:00"))

    print_schedule(Scheduler(owner))


if __name__ == "__main__":
    main()
