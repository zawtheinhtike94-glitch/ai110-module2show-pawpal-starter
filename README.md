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

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Output of `python main.py` (one owner with 90 minutes, two pets, six tasks):

```
========================================================
  Today's Schedule for Jordan (90 min available)
========================================================
  Time   Task              Pet        Min  Priority
  ----------------------------------------------------
  07:30  Morning walk      Biscuit     30  high
  08:00  Breakfast         Biscuit     10  high
  08:15  Feeding           Mochi       10  high
  09:00  Medication        Mochi        5  medium
  18:00  Play session      Mochi       20  medium
  ----------------------------------------------------
  Total: 75 of 90 min

  Skipped (not enough time):
    - Bath for Biscuit (45 min, low)

Why this plan:
Jordan has 90 minutes today.
Included 'Morning walk' for Biscuit: high priority, 30 min (total so far 30 min).
Included 'Breakfast' for Biscuit: high priority, 10 min (total so far 40 min).
Included 'Feeding' for Mochi: high priority, 10 min (total so far 50 min).
Included 'Medication' for Mochi: medium priority, 5 min (total so far 55 min).
Included 'Play session' for Mochi: medium priority, 20 min (total so far 75 min).
Skipped 'Bath' for Biscuit: needs 45 min but not enough time was left after higher-priority tasks.
```

## 🧩 Implementation Summary

PawPal+ is built from four classes in `pawpal_system.py`. An **Owner** has a name, the minutes they have available today, and a list of **Pets**; each Pet holds its own list of care **Tasks** (title, duration, priority, preferred time, frequency, and completion status).

The **Scheduler** is the "brain": it gets every pet's tasks through `Owner.get_all_tasks()`, skips completed ones, sorts the rest by priority (then by preferred time), and adds tasks to the plan until the owner's available time runs out. Tasks that don't fit go into a skipped list, and `explain_plan()` describes why each task was included or skipped. `main.py` is a demo script that builds a sample owner with two pets and prints today's schedule.

## 🧪 Testing PawPal+

Run the full test suite from the project folder (with `.venv` activated):

```bash
python -m pytest
```

The tests in `tests/test_pawpal.py` cover:

- **Basics:** `mark_complete()` marks a task done, and adding a task increases a pet's task count.
- **Sorting:** `sort_by_time()` returns tasks in chronological order, with untimed tasks last.
- **Recurring tasks:** completing a daily task creates a new copy due tomorrow; a weekly task's copy is due in 7 days.
- **Conflict detection:** two tasks at the same time (even for different pets) produce a warning; different times produce none.
- **Scheduling edge cases:** pets with no tasks give an empty plan, and when time runs out, high-priority tasks are kept and lower-priority ones are skipped.

Sample test output:

```
============================= test session starts ==============================
platform darwin -- Python 3.13.15, pytest-9.1.1, pluggy-1.7.0
collected 9 items

tests/test_pawpal.py .........                                           [100%]

============================== 9 passed in 0.01s ===============================
```

**Confidence level: ⭐⭐⭐⭐ (4/5).** All 9 tests pass and cover the main scheduling behaviors and several edge cases. It isn't 5 stars because some things aren't tested yet: overlapping task durations (only exact time matches are flagged as conflicts), invalid time formats like "8am", and the Streamlit UI itself.

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()`, `Scheduler.sort_by_priority()` | `sort_by_time()` orders tasks by their "HH:MM" time (tasks with no time go last). `sort_by_priority()` puts high before medium before low, breaking ties by time. |
| Filtering | `Scheduler.filter_tasks()`, `Scheduler.generate_plan()` | `filter_tasks()` returns tasks for one pet and/or by completion status. `generate_plan()` leaves out completed or future tasks and skips tasks once the owner's available minutes run out. |
| Conflict handling | `Scheduler.detect_conflicts()` | Returns a warning message (instead of crashing) when two or more tasks share the exact same start time, across all pets. Overlapping durations are not checked (see reflection 2b). |
| Recurring tasks | `Task.mark_complete()`, `Scheduler.mark_task_complete()` | Completing a daily task creates a new copy due tomorrow (+1 day); a weekly task creates one due in 7 days, using `timedelta`. The new copy is added to the same pet. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
