"""Tests for the core PawPal+ classes and scheduling logic."""

from datetime import date, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def make_owner(minutes=60):
    """Create an owner with two pets (no tasks yet) for the scheduler tests."""
    owner = Owner("Jordan", available_minutes=minutes)
    owner.add_pet(Pet("Biscuit", "dog", 3))
    owner.add_pet(Pet("Mochi", "cat", 5))
    return owner


def test_mark_complete_changes_status():
    """Calling mark_complete() should set completed to True."""
    task = Task("Morning walk", 30, "high")
    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_pet_task_count():
    """Adding a task to a pet should increase that pet's task count by one."""
    pet = Pet("Biscuit", "dog", 3)
    assert len(pet.get_tasks()) == 0

    pet.add_task(Task("Breakfast", 10, "high"))

    assert len(pet.get_tasks()) == 1


def test_sort_by_time_returns_chronological_order():
    """Tasks added out of order come back in clock order, with untimed tasks last."""
    scheduler = Scheduler(make_owner())
    tasks = [
        Task("Play", 20, time="18:00"),
        Task("Brush", 5),
        Task("Walk", 30, time="07:30"),
        Task("Meds", 5, time="09:00"),
    ]

    result = scheduler.sort_by_time(tasks)

    assert [task.title for task in result] == ["Walk", "Meds", "Play", "Brush"]


def test_completing_daily_task_creates_one_for_tomorrow():
    """Marking a daily task complete adds a new, unfinished copy due the next day."""
    owner = make_owner()
    biscuit = owner.get_pets()[0]
    walk = Task("Walk", 30, "high", time="08:00", frequency="daily")
    biscuit.add_task(walk)

    Scheduler(owner).mark_task_complete(walk)

    tasks = biscuit.get_tasks()
    assert len(tasks) == 2
    next_walk = tasks[1]
    assert next_walk.title == "Walk"
    assert next_walk.completed is False
    assert next_walk.due_date == date.today() + timedelta(days=1)


def test_completing_weekly_task_creates_one_for_next_week():
    """A weekly task's next copy is due 7 days later."""
    owner = make_owner()
    mochi = owner.get_pets()[1]
    bath = Task("Bath", 20, "low", frequency="weekly")
    mochi.add_task(bath)

    next_bath = Scheduler(owner).mark_task_complete(bath)

    assert next_bath.due_date == date.today() + timedelta(weeks=1)


def test_detect_conflicts_flags_same_time_across_pets():
    """Two tasks at the same time (even for different pets) produce a warning."""
    owner = make_owner()
    biscuit, mochi = owner.get_pets()
    biscuit.add_task(Task("Breakfast", 10, time="08:00"))
    mochi.add_task(Task("Feeding", 10, time="08:00"))
    mochi.add_task(Task("Meds", 5, time="09:00"))

    warnings = Scheduler(owner).detect_conflicts()

    assert len(warnings) == 1
    assert "08:00" in warnings[0]


def test_no_conflicts_when_times_differ():
    """Edge case: tasks at different times produce no warnings."""
    owner = make_owner()
    owner.get_pets()[0].add_task(Task("Walk", 30, time="07:30"))
    owner.get_pets()[1].add_task(Task("Feeding", 10, time="08:00"))

    assert Scheduler(owner).detect_conflicts() == []


def test_plan_is_empty_when_pets_have_no_tasks():
    """Edge case: an owner whose pets have no tasks gets an empty plan."""
    scheduler = Scheduler(make_owner())

    assert scheduler.generate_plan() == []
    assert scheduler.skipped_tasks == []


def test_plan_skips_tasks_that_do_not_fit():
    """High-priority tasks are planned first; a task that doesn't fit the time left is skipped."""
    owner = make_owner(minutes=40)
    biscuit = owner.get_pets()[0]
    biscuit.add_task(Task("Bath", 30, "low"))
    biscuit.add_task(Task("Walk", 30, "high"))
    biscuit.add_task(Task("Feeding", 10, "high"))

    scheduler = Scheduler(owner)
    plan = scheduler.generate_plan()

    assert [task.title for task in plan] == ["Walk", "Feeding"]
    assert [task.title for task in scheduler.skipped_tasks] == ["Bath"]
