import streamlit as st

from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Owner")
owner_name = st.text_input("Owner name", value="Jordan")
available_minutes = st.number_input("Minutes available today", min_value=1, max_value=1440, value=60)

# Streamlit reruns this file on every click, so keep the Owner in session_state
# instead of creating a new (empty) one each time.
if "owner" not in st.session_state:
    st.session_state.owner = Owner(owner_name, available_minutes=int(available_minutes))

owner = st.session_state.owner
owner.name = owner_name
owner.available_minutes = int(available_minutes)

st.markdown("### Pets")
col1, col2, col3 = st.columns(3)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "other"])
with col3:
    pet_age = st.number_input("Age", min_value=0, max_value=40, value=3)

if st.button("Add pet"):
    if any(pet.name == pet_name for pet in owner.get_pets()):
        st.warning(f"{pet_name} is already added.")
    else:
        owner.add_pet(Pet(pet_name, species, int(pet_age)))
        st.success(f"Added {pet_name}!")

if owner.get_pets():
    st.table([{"name": p.name, "species": p.species, "age": p.age, "tasks": len(p.get_tasks())} for p in owner.get_pets()])
else:
    st.info("No pets yet. Add one above.")

st.markdown("### Tasks")

if not owner.get_pets():
    st.caption("Add a pet first, then you can give it tasks.")
else:
    pet_names = [pet.name for pet in owner.get_pets()]
    col1, col2 = st.columns(2)
    with col1:
        task_pet = st.selectbox("For pet", pet_names)
        task_title = st.text_input("Task title", value="Morning walk")
        task_time = st.text_input("Preferred time (HH:MM, optional)", value="08:00")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
        frequency = st.selectbox("Frequency", ["daily", "weekly"])

    if st.button("Add task"):
        pet = next(p for p in owner.get_pets() if p.name == task_pet)
        pet.add_task(
            Task(task_title, int(duration), priority, time=task_time.strip() or None, frequency=frequency)
        )
        st.success(f"Added '{task_title}' for {task_pet}.")

scheduler = Scheduler(owner)

if owner.get_all_tasks():
    # Conflict warnings: shown right above the task list so the owner can fix them before planning.
    for warning in scheduler.detect_conflicts():
        st.warning(f"⚠️ {warning} Consider moving one of them to a different time.")

    st.markdown("#### Task list")
    col1, col2 = st.columns(2)
    with col1:
        pet_filter = st.selectbox("Show tasks for", ["All pets"] + [p.name for p in owner.get_pets()])
    with col2:
        status_filter = st.radio("Status", ["All", "To do", "Done"], horizontal=True)

    completed = {"All": None, "To do": False, "Done": True}[status_filter]
    filtered = scheduler.filter_tasks(
        pet_name=None if pet_filter == "All pets" else pet_filter, completed=completed
    )
    shown = scheduler.sort_by_time(filtered)

    if shown:
        st.caption("Sorted by time (tasks with no time are listed last).")
        st.table(
            [
                {
                    "time": t.time or "any",
                    "pet": t.pet_name,
                    "task": t.title,
                    "minutes": t.duration_minutes,
                    "priority": t.priority,
                    "repeats": t.frequency,
                    "due": t.due_date.isoformat(),
                    "status": "✅ done" if t.completed else "to do",
                }
                for t in shown
            ]
        )
    else:
        st.info("No tasks match this filter.")

    # Completing a task through the Scheduler also creates the next copy of a daily/weekly task.
    open_tasks = scheduler.sort_by_time(scheduler.filter_tasks(completed=False))
    if open_tasks:
        labels = [f"{t.time or 'any'} · {t.title} ({t.pet_name}) · due {t.due_date.isoformat()}" for t in open_tasks]
        col1, col2 = st.columns([3, 1])
        with col1:
            choice = st.selectbox("Mark a task as done", range(len(open_tasks)), format_func=lambda i: labels[i])
        with col2:
            st.write("")
            st.write("")
            if st.button("Mark done"):
                task = open_tasks[choice]
                next_task = scheduler.mark_task_complete(task)
                if next_task is not None:
                    st.session_state.flash = (
                        f"Marked '{task.title}' done. Next {task.frequency} copy is due {next_task.due_date.isoformat()}."
                    )
                else:
                    st.session_state.flash = f"Marked '{task.title}' done."
                st.rerun()

    if "flash" in st.session_state:
        st.success(st.session_state.pop("flash"))
elif owner.get_pets():
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Uses the Scheduler to fit the highest-priority tasks into your available time.")

if st.button("Generate schedule"):
    plan = scheduler.generate_plan()

    if not plan and not scheduler.skipped_tasks:
        st.warning("Nothing to schedule yet. Add a pet and some tasks first.")
    else:
        used = sum(t.duration_minutes for t in plan)
        st.success(f"Planned {len(plan)} task(s) using {used} of {owner.available_minutes} minutes.")
        if plan:
            st.table(
                [
                    {
                        "time": t.time or "any",
                        "task": t.title,
                        "pet": t.pet_name,
                        "minutes": t.duration_minutes,
                        "priority": t.priority,
                    }
                    for t in scheduler.sort_by_time(plan)
                ]
            )
            st.caption("Tasks are chosen by priority, then shown in time order.")
        for warning in scheduler.detect_conflicts():
            st.warning(f"⚠️ {warning}")
        if scheduler.skipped_tasks:
            st.warning(
                "Skipped (not enough time): "
                + ", ".join(f"{t.title} for {t.pet_name}" for t in scheduler.skipped_tasks)
            )
        with st.expander("Why this plan?"):
            st.text(scheduler.explain_plan())
