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

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
