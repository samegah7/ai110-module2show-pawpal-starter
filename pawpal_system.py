from dataclasses import dataclass, field
from typing import List
from datetime import date


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: List["Task"] = field(default_factory=list)

    def get_info(self) -> str:
        """Return a formatted string with the pet's name, species, and age."""
        return f"{self.name} ({self.species}, {self.age} yr{'s' if self.age != 1 else ''} old)"


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str          # "low", "medium", "high"
    frequency: str = "daily"   # e.g. "daily", "weekly", "as needed"
    completed: bool = False
    pet: "Pet" = None

    def is_high_priority(self) -> bool:
        """Return True if the task's priority is 'high'."""
        return self.priority == "high"

    def mark_complete(self):
        """Mark the task as completed by setting completed to True."""
        self.completed = True

    def __str__(self) -> str:
        """Return a human-readable summary of the task."""
        status = "done" if self.completed else "pending"
        pet_label = f" [{self.pet.name}]" if self.pet else ""
        return (
            f"[{self.priority.upper()}]{pet_label} {self.title} "
            f"({self.duration_minutes} min, {self.frequency}) — {status}"
        )


class Owner:
    def __init__(self, name: str):
        self.name = name
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet):
        """Add a Pet to this owner's list of pets."""
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        """Return every task across all pets owned by this owner."""
        all_tasks: List[Task] = []
        for pet in self.pets:
            if hasattr(pet, "tasks"):
                all_tasks.extend(pet.tasks)
        return all_tasks

    def __str__(self) -> str:
        """Return a string listing the owner's name and all their pets."""
        pet_names = ", ".join(p.name for p in self.pets) if self.pets else "none"
        return f"Owner: {self.name} | Pets: {pet_names}"


class Scheduler:
    PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}

    def __init__(self, owner: Owner, available_minutes: int):
        self.owner = owner
        self.tasks: List[Task] = []
        self.available_minutes = available_minutes

    def add_task(self, task: Task):
        """Register a task with the scheduler for inclusion in the plan."""
        self.tasks.append(task)

    def sort_tasks(self):
        """Sort tasks by priority (high → medium → low), then by duration."""
        self.tasks.sort(
            key=lambda t: (self.PRIORITY_ORDER.get(t.priority, 99), t.duration_minutes)
        )

    def generate_schedule(self) -> "ScheduledPlan":
        """Fit as many tasks as possible into available_minutes, highest priority first."""
        self.sort_tasks()
        plan = ScheduledPlan(date=str(date.today()))
        remaining = self.available_minutes

        for task in self.tasks:
            if task.completed:
                continue
            if task.duration_minutes <= remaining:
                plan.add_task(task)
                remaining -= task.duration_minutes

        return plan

    def explain_plan(self):
        plan = self.generate_schedule()
        print(f"\n=== PawPal Schedule for {self.owner.name} ===")
        print(f"Available time : {self.available_minutes} min")
        print(f"Scheduled      : {plan.total_time} min across {len(plan.tasks)} task(s)")
        skipped = len([t for t in self.tasks if t not in plan.tasks and not t.completed])
        if skipped:
            print(f"Skipped (no time): {skipped} task(s)")
        plan.display()


class ScheduledPlan:
    def __init__(self, date: str):
        self.date = date
        self.tasks: List[Task] = []
        self.total_time: int = 0

    def add_task(self, task: Task):
        self.tasks.append(task)
        self.total_time += task.duration_minutes

    def display(self):
        """Print all scheduled tasks and the total time to the terminal."""
        print(f"\n--- Plan for {self.date} ({self.total_time} min total) ---")
        if not self.tasks:
            print("  No tasks scheduled.")
            return
        for i, task in enumerate(self.tasks, start=1):
            print(f"  {i}. {task}")
