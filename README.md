# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Smarter Scheduling

The scheduler has been extended beyond basic greedy time-filling with four algorithmic improvements:

**Sort by time** — `Scheduler.sort_by_time()` returns tasks ordered by their `"HH:MM"` start time using `sorted()` with a lambda key. Tasks with no time set fall to the end. This makes the daily plan read like a real timeline instead of a priority dump.

**Filter by pet or status** — `filter_by_pet(name)` and `filter_by_status(completed)` let you query the task list without touching the schedule. Useful for showing only one pet's workload or surfacing everything still pending.

**Recurring task automation** — `Scheduler.mark_task_complete(task)` marks a task done and, for `"daily"` or `"weekly"` tasks, automatically creates the next occurrence using Python's `timedelta`. The new task is registered on both the pet and the scheduler with a `next_due_date` set — no manual re-entry needed. `"as needed"` tasks do not auto-recur.

**Time conflict detection** — `warn_time_conflicts()` groups pending tasks by exact start time and returns a plain-English warning string for every clash. It never raises an exception — if there are no conflicts the list is empty. Note: it detects same start-time collisions only, not overlapping durations (see `reflection.md` section 2b for the reasoning).

---

## Testing PawPal+

### Run the test suite

```bash
python -m pytest tests/test_pawpal.py -v
```

### What the tests cover

| Area | Description |
|---|---|
| **Sorting correctness** | Verifies tasks are ordered high → medium → low priority, and that `sort_by_time()` returns tasks in chronological HH:MM order with untimed tasks placed last. |
| **Recurrence logic** | Confirms that completing a `daily` task creates a new task due tomorrow, a `weekly` task creates one due in 7 days, an `as needed` task produces no recurrence, and tasks without a pet assigned do not crash. |
| **Conflict detection** | Checks that two pending tasks at the same start time trigger a warning, that completed tasks are excluded from conflict checks, and that tasks with no time set never produce false positives. |
| **Edge cases** | A pet with zero tasks does not crash the scheduler; a single task whose duration exceeds the available time budget is excluded from the generated plan. |

### Confidence level

★★★★☆ (4 / 5)

All 15 tests pass. Core scheduling, recurrence, and conflict-detection paths are covered with both happy-path and edge-case scenarios. The one gap is overlapping-duration detection — `warn_time_conflicts` currently catches only exact same-start-time clashes, not tasks whose time windows overlap — which is noted in `reflection.md`.

---

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
