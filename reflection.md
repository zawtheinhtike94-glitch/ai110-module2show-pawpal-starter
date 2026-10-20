# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

Core user actions:
1. A user can enter their owner info and add a pet with its name, species, and age.
2. A user can add or edit a care task (like a walk, feeding, or medication) with how long it takes and how important it is.
3. A user can generate today's plan, which lists the tasks in order and explains why it chose that order.

- **Briefly describe your initial UML design.**
  My UML has four classes connected in a chain: an Owner has many Pets, each Pet has many Tasks, and a Scheduler uses the Owner to reach every pet and task so it can build the daily plan. I kept the data (Owner, Pet, Task) separate from the planning logic (Scheduler) so each class has one clear job.

- **What classes did you include, and what responsibilities did you assign to each?**
  - **Owner**: holds the owner's name, how many minutes they have available today, their preferences, and their list of pets. It can add, remove, and list pets.
  - **Pet**: holds the pet's name, species, age, and its care tasks. It can add, remove, and list its tasks.
  - **Task**: one care activity (walk, feeding, meds, grooming). It stores the title, duration, priority, optional preferred time, frequency (daily/weekly), and whether it's completed. It can be marked complete or edited.
  - **Scheduler**: the "brain" of the app. It looks at all tasks across the owner's pets, sorts them by priority, picks the ones that fit in the available time, and explains its choices.

**b. Design changes**

- **Did your design change during implementation?**
  Yes. After drafting the skeleton, I asked my AI assistant (Claude) to review `pawpal_system.py` for missing relationships or logic bottlenecks.

- **If yes, describe at least one change and why you made it.**
  The review pointed out that `explain_plan()` had no way to know which tasks were skipped, because `generate_plan()` only returned the chosen tasks. I added two lists to the Scheduler, `planned_tasks` and `skipped_tasks`, so the plan's results are saved and `explain_plan()` can say why each task was included or left out. I updated the UML to match.

  The review also noted that `priority` is stored as text ("low"/"medium"/"high"), which can't be sorted correctly alphabetically. I decided not to change the type yet; instead I'll map each priority to a number inside `sort_by_priority()` in Phase 2. It also mentioned that a Task doesn't know which Pet it belongs to, so the plan can't show the pet's name next to each task. I'm keeping that in mind for Phase 2 rather than adding it now, to keep the first design simple.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- **What constraints does your scheduler consider (for example: time, priority, preferences)?**
  The scheduler considers four things: (1) **available time**, meaning the owner's minutes for today, which is a hard limit; (2) **priority**, so high tasks are planned before medium and low ones; (3) **preferred time**, which breaks ties between tasks with the same priority and is used to sort the final plan and detect conflicts; and (4) **status and due date**, so completed tasks and future copies of recurring tasks are left out of today's plan.

- **How did you decide which constraints mattered most?**
  I ranked them by what would hurt the pet most if it went wrong. Time comes first because a plan the owner can't actually finish isn't useful. Priority comes next because things like feeding and medication matter more than a bath or extra play, so when time runs out, the low-priority tasks should be the ones skipped. Preferred time comes last because most pet tasks are flexible by a few minutes. I store owner `preferences` but don't use them in the scheduling logic yet, to keep the first version simple.

**b. Tradeoffs**

- **Describe one tradeoff your scheduler makes.**
  My conflict detection (`Scheduler.detect_conflicts()`) only flags tasks that have the exact same start time, like two tasks both at 08:00. It does not check whether tasks overlap based on their durations. For example, a 30-minute walk at 07:30 and a feeding at 07:45 really do overlap, but my scheduler won't warn about them.

- **Why is that tradeoff reasonable for this scenario?**
  For a busy pet owner, the most common mistake is accidentally putting two things in the same time slot, and the exact-match check catches that with simple, easy-to-read code (group tasks by time, warn if a slot has more than one). Many pet tasks are also flexible; a feeding can usually happen a few minutes after a walk ends. Checking real overlaps would mean converting times to minutes and comparing every pair of tasks, which adds complexity for a small benefit right now. If users needed tighter timing, overlap checking would be the next improvement.

---

## 3. AI Collaboration

**a. How you used AI**

- **How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?**
  I used Claude as my coding assistant for almost every step. It helped me brainstorm the four classes and their attributes and methods, turned that list into a Mermaid.js UML diagram, generated the class skeleton in `pawpal_system.py`, filled in the method logic, wrote the `main.py` demo script, and drafted my first two pytest tests. I also used it as a tutor: I asked it to explain what UML is, why I need to activate a virtual environment, and why we write tests at all.

- **What kinds of prompts or questions were most helpful?**
  Short, specific requests worked best, like "write each box from the diagram as a Python class" or "review this skeleton for missing relationships." Asking "why" questions ("why do I have to activate the venv?") was also helpful because the answers helped me understand the steps instead of just copying commands.

**b. Judgment and verification**

- **Describe one moment where you did not accept an AI suggestion as-is.**
  When the AI reviewed my skeleton, it pointed out that `priority` was stored as text ("low"/"medium"/"high"), which would sort in the wrong order alphabetically. Instead of changing the attribute to a number right away, I kept it as readable text and decided to map each priority to a number only inside `sort_by_priority()`. It also suggested linking each Task to its Pet; I waited until Phase 2 to add `pet_name`, when I actually needed it to show the pet's name in the schedule.

- **How did you evaluate or verify what the AI suggested?**
  I checked the UML by pasting it into mermaid.live and making sure the arrows (Owner has Pets, Pet has Tasks, Scheduler uses Owner) matched my design. I verified the code by running `python main.py` and checking that the high-priority tasks came first and that the 45-minute bath was skipped when there wasn't enough time left. Finally, I ran `python -m pytest` and confirmed both tests passed.

---

## 4. Testing and Verification

**a. What you tested**

- **What behaviors did you test?**
  My 9 pytest tests in `tests/test_pawpal.py` cover: marking a task complete; adding a task to a pet; sorting tasks into chronological order (with untimed tasks last); a daily task creating a new copy due tomorrow and a weekly task creating one due in 7 days; conflict detection flagging two tasks at 08:00 for different pets; no false warning when times differ; an empty plan when pets have no tasks; and the plan keeping high-priority tasks and skipping a low-priority one when time runs out.

- **Why were these tests important?**
  These are the behaviors a pet owner actually relies on. If sorting or recurrence broke, a feeding or medication could be missed or show up on the wrong day. The edge-case tests (no tasks, not enough time, no conflicts) check that the app doesn't crash or give misleading warnings in situations that are easy to hit in real use. Having them also let me change `pawpal_system.py` in later phases and quickly confirm I didn't break earlier features.

**b. Confidence**

- **How confident are you that your scheduler works correctly?**
  About 4 out of 5. All 9 tests pass, `main.py` produces the expected schedule, and I tried the main flows by hand in the Streamlit app (adding pets and tasks, seeing a conflict warning, marking a task done, generating a plan).

- **What edge cases would you test next if you had more time?**
  Overlapping durations (a 30-minute walk at 07:30 and a feeding at 07:45), invalid time input like "8am" or "25:00", a task longer than all the available time, two pets with the same name, marking the same task done twice, and automated tests for the Streamlit UI itself.

---

## 5. Reflection

**a. What went well**

- **What part of this project are you most satisfied with?**
  I'm most satisfied that the whole system fits together: the same `Scheduler` methods power both the terminal demo and the web app, and the app now shows sorting, filtering, conflict warnings, and recurring tasks instead of just a static form. The "Why this plan?" explanation is also a part I like, because it makes the scheduler's choices easy to understand.

**b. What you would improve**

- **If you had another iteration, what would you improve or redesign?**
  I would check for overlapping durations instead of only exact time matches, validate the time input so "8am" can't be entered, and actually use the owner's preferences (for example, putting walks in the morning). I'd also save the data to a file so pets and tasks aren't lost when the app restarts, since right now they only live in `st.session_state`.

**c. Key takeaway**

- **What is one important thing you learned about designing systems or working with AI on this project?**
  Designing first made everything after it easier. Because the UML and class skeleton were clear, each later feature had an obvious place to go (for example, all the smart logic belongs in `Scheduler`). I also learned that AI can write a lot of code quickly, but I still have to be the one who checks it: running `main.py`, running pytest, and trying the app myself is how I knew the code actually worked.

**d. AI strategy and being the lead architect**

- **Which AI coding assistant features were most effective for building your scheduler?**
  Having the assistant edit files directly and then run the code to check it was the most effective. For example, after it added `detect_conflicts()`, it ran `main.py` and pytest right away so I could see the 08:00 warning and "9 passed". It was also useful that it could read the course instructions and my files together, so its suggestions matched the project requirements (like making the Scheduler use `Owner.get_all_tasks()`).

- **Give one example of an AI suggestion you rejected or modified to keep your system design clean.**
  The AI pointed out that storing `priority` as text would sort in the wrong order. Instead of turning priority into numbers everywhere, I kept the readable "low/medium/high" values and only mapped them to numbers inside `sort_by_priority()`, so the rest of the code and the UI stayed simple.

- **How did using separate chat sessions for different phases help you stay organized?**
  I actually did most of the project in one long chat session instead of separate ones. What kept me organized was working one phase and one step at a time and committing to GitHub after each step, so my commit history matches the phases. In hindsight, separate sessions per phase would have kept each conversation shorter and more focused, and I'd try that next time.

- **What did you learn about being the "lead architect" when collaborating with powerful AI tools?**
  The AI is fast at writing code, but it doesn't know what matters for my users unless I decide that. My job was to set the design, choose the tradeoffs (like exact-time conflict checks), and verify the results. One example: after an update, the app crashed with "Scheduler has no attribute detect_conflicts". The code was correct, but the running Streamlit server was still using the old file. Understanding that and restarting the app was something I had to figure out and check myself.
