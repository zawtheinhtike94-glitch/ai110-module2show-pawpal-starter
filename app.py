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

all_tasks = owner.get_all_tasks()
if all_tasks:
    st.write("Current tasks:")
    st.table(
        [
            {
                "pet": t.pet_name,
                "task": t.title,
                "time": t.time or "any",
                "minutes": t.duration_minutes,
                "priority": t.priority,
                "frequency": t.frequency,
            }
            for t in all_tasks
        ]
    )
elif owner.get_pets():
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Uses the Scheduler to fit the highest-priority tasks into your available time.")

if st.button("Generate schedule"):
    scheduler = Scheduler(owner)
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
                    for t in plan
                ]
            )
        if scheduler.skipped_tasks:
            st.warning(
                "Skipped (not enough time): "
                + ", ".join(f"{t.title} for {t.pet_name}" for t in scheduler.skipped_tasks)
            )
        with st.expander("Why this plan?"):
            st.text(scheduler.explain_plan())
