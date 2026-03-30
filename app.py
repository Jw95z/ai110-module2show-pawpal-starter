import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")


if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan")

if "selected_pet_name" not in st.session_state:
    st.session_state.selected_pet_name = None

owner = st.session_state.owner
scheduler = Scheduler(owner)

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to PawPal+.

This version connects the Streamlit interface to your backend classes so pets and tasks
are stored using your Python system design.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.
"""
    )

st.divider()


st.subheader("Owner")
owner_name_input = st.text_input("Owner name", value=owner.name)

if st.button("Update owner name"):
    owner.name = owner_name_input
    st.success(f"Owner name updated to {owner.name}")

st.divider()


st.subheader("Add a Pet")

with st.form("add_pet_form"):
    pet_name = st.text_input("Pet name")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    age = st.number_input("Age", min_value=0, max_value=50, value=0)
    add_pet_submitted = st.form_submit_button("Add pet")

if add_pet_submitted:
    if pet_name.strip():
        new_pet = Pet(name=pet_name.strip(), species=species, age=int(age))
        owner.add_pet(new_pet)
        st.success(f"Added pet: {new_pet.name}")
    else:
        st.error("Please enter a pet name.")


st.subheader("Current Pets")

pets = owner.get_pets()

if pets:
    pet_names = [pet.name for pet in pets]
    selected_pet_name = st.selectbox("Choose a pet", pet_names)
    st.session_state.selected_pet_name = selected_pet_name

    selected_pet = next(p for p in pets if p.name == selected_pet_name)
    st.write(
        f"**{selected_pet.name}** ({selected_pet.species}), age {selected_pet.age}"
    )
else:
    selected_pet = None
    st.info("No pets added yet.")

st.divider()

st.subheader("Add a Task")

if selected_pet is not None:
    with st.form("add_task_form"):
        task_description = st.text_input("Task description", value="Morning walk")
        task_time = st.text_input("Time (HH:MM)", value="08:00")
        task_frequency = st.selectbox("Frequency", ["daily", "weekly", "as needed"])
        add_task_submitted = st.form_submit_button("Add task")

    if add_task_submitted:
        if task_description.strip() and task_time.strip():
            new_task = Task(
                description=task_description.strip(),
                time=task_time.strip(),
                frequency=task_frequency,
            )
            selected_pet.add_task(new_task)
            st.success(f"Added task to {selected_pet.name}: {new_task.description}")
        else:
            st.error("Please fill in both the task description and time.")
else:
    st.info("Add a pet first before adding tasks.")

st.divider()

st.subheader("Tasks")

if pets:
    any_tasks = False
    for pet in pets:
        st.markdown(f"### {pet.name}")
        if pet.tasks:
            any_tasks = True
            task_rows = []
            for task in pet.tasks:
                task_rows.append(
                    {
                        "Description": task.description,
                        "Time": task.time,
                        "Frequency": task.frequency,
                        "Status": task.get_status(),
                    }
                )
            st.table(task_rows)
        else:
            st.caption("No tasks yet for this pet.")

    if not any_tasks:
        st.info("No tasks added yet.")
else:
    st.info("No pets available.")

st.divider()
st.subheader("Today's Schedule")

if st.button("Generate schedule"):
    schedule = scheduler.get_todays_schedule()

    if schedule:
        for pet, task in schedule:
            st.write(
                f"**{task.time}** — {pet.name} ({pet.species}): "
                f"{task.description} [{task.frequency}] - {task.get_status()}"
            )
    else:
        st.warning("No tasks scheduled yet.")

st.divider()

st.subheader("Mark Task Complete")

all_schedule = scheduler.get_todays_schedule()

if all_schedule:
    task_options = [
        f"{pet.name} | {task.time} | {task.description}"
        for pet, task in all_schedule
    ]

    selected_task_label = st.selectbox("Select a task to mark complete", task_options)

    if st.button("Mark selected task complete"):
        pet_name, task_time, task_description = selected_task_label.split(" | ", 2)
        updated = scheduler.mark_task_complete(
            pet_name=pet_name,
            description=task_description,
            time=task_time,
        )

        if updated:
            st.success("Task marked complete.")
        else:
            st.error("Could not find that task.")
else:
    st.info("No tasks available to mark complete.")