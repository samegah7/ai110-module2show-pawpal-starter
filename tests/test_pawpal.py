import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pawpal_system import Pet, Task


def test_mark_complete_changes_status():
    """Calling mark_complete() should set completed to True."""
    task = Task(title="Walk", duration_minutes=20, priority="high")
    assert task.completed == False
    task.mark_complete()
    assert task.completed == True


def test_adding_task_increases_pet_task_count():
    """Adding a task to a Pet's task list should increase the count by 1."""
    pet = Pet(name="Biscuit", species="Dog", age=3)
    assert len(pet.tasks) == 0
    task = Task(title="Feed", duration_minutes=10, priority="medium", pet=pet)
    pet.tasks.append(task)
    assert len(pet.tasks) == 1
