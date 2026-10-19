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

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | | e.g., by priority, duration |
| Filtering | | e.g., skip tasks if time runs out |
| Conflict handling | | e.g., overlapping time slots |
| Recurring tasks | | e.g., daily vs. weekly |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
