"""Quick tests for the core PawPal+ classes."""

from pawpal_system import Pet, Task


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
