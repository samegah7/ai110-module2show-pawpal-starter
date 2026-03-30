from dataclasses import dataclass
from typing import List


@dataclass
class Pet:
    name: str
    species: str
    age: int

    def get_info(self):
        pass


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str  # "low", "medium", "high"

    def is_high_priority(self):
        pass


class Owner:
    def __init__(self, name: str):
        self.name = name
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet):
        pass


class Scheduler:
    def __init__(self, owner: Owner, available_minutes: int):
        self.owner = owner
        self.tasks: List[Task] = []
        self.available_minutes = available_minutes

    def add_task(self, task: Task):
        pass

    def generate_schedule(self):
        pass

    def explain_plan(self):
        pass


class ScheduledPlan:
    def __init__(self, date: str):
        self.date = date
        self.tasks: List[Task] = []
        self.total_time: int = 0

    def display(self):
        pass
