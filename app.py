import streamlit as st
from datetime import date
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# ---------------------------
# Session state setup
# ---------------------------
if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan")

owner = st.session_state.owner
scheduler = Scheduler(owner)

st.title("🐾 PawPal+")

st.markdown(
    """
PawPal+ helps pet owners manage care tasks, generate a daily plan,
and detect simple scheduling conflicts.
"""
)

st.divider()

# ---------------------------
# Owner section
# ---------------------------
st.subheader("Owner Info")
owner_name = st.text_input("Owner name", value=owner.name)

if st.button("Update owner name"):
    owner.name = owner_name.strip()
    st.success(f"Owner name updated to {owner.name}")

st.divider()

# ---------------------------
# Add pet section
# ---------------------------
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

pets = owner.get_pets()

st.divider()

# ---------------------------
# Pet selection
# ---------------------------
st.subheader("Current Pets")

selected_pet = None

if pets:
    pet_names = [pet.name for pet in pets]
    selected_pet_name = st.selectbox("Choose a pet", pet_names)
    selected_pet = next((pet for pet in pets if pet.name == selected_pet_name), None)

    if selected_pet:
        st.info(
            f"Selected pet: {selected_pet.name} ({selected_pet.species}), age {selected_pet.age}"
        )
else:
    st.info("No pets added yet.")

st.divider()

# ---------------------------
# Add task section
# ---------------------------
st.subheader("Add a Task")

if selected_pet:
    with st.form("add_task_form"):
        task_description = st.text_input("Task description", value="Morning walk")
        task_time = st.text_input("Time (HH:MM)", value="08:00")
        task_frequency = st.selectbox("Frequency", ["daily", "weekly", "once"])
        add_task_submitted = st.form_submit_button("Add task")

    if add_task_submitted:
        if task_description.strip() and task_time.strip():
            new_task = Task(
                description=task_description.strip(),
                time=task_time.strip(),
                frequency=task_frequency,
                due_date=date.today(),
            )
            selected_pet.add_task(new_task)
            st.success(f"Added task to {selected_pet.name}: {new_task.description}")
        else:
            st.error("Please fill in both task description and time.")
else:
    st.info("Add a pet first before adding tasks.")

st.divider()

# ---------------------------
# Filter section
# ---------------------------
st.subheader("Task Filters")

filter_pet = st.selectbox(
    "Filter by pet",
    ["All"] + [pet.name for pet in pets] if pets else ["All"]
)

filter_status = st.selectbox(
    "Filter by status",
    ["All", "Pending", "Done"]
)

pet_name_filter = None if filter_pet == "All" else filter_pet
completed_filter = None
if filter_status == "Pending":
    completed_filter = False
elif filter_status == "Done":
    completed_filter = True

filtered_tasks = scheduler.filter_tasks(
    pet_name=pet_name_filter,
    completed=completed_filter,
)

st.subheader("Filtered Tasks")

if filtered_tasks:
    rows = []
    for pet, task in filtered_tasks:
        rows.append(
            {
                "Pet": pet.name,
                "Species": pet.species,
                "Task": task.description,
                "Date": task.due_date.isoformat(),
                "Time": task.time,
                "Frequency": task.frequency,
                "Status": task.get_status(),
            }
        )
    st.table(rows)
else:
    st.info("No tasks match the selected filters.")

st.divider()

# ---------------------------
# Schedule section
# ---------------------------
st.subheader("Today's Schedule")

today_schedule = scheduler.get_todays_schedule()

if today_schedule:
    schedule_rows = []
    for pet, task in today_schedule:
        schedule_rows.append(
            {
                "Time": task.time,
                "Pet": pet.name,
                "Species": pet.species,
                "Task": task.description,
                "Frequency": task.frequency,
                "Status": task.get_status(),
            }
        )
    st.table(schedule_rows)
else:
    st.info("No tasks scheduled for today.")

# Conflict warnings
warnings = scheduler.detect_conflicts(today_schedule)
if warnings:
    st.warning("Scheduling conflicts detected:")
    for warning in warnings:
        st.warning(warning)
else:
    st.success("No scheduling conflicts detected for today.")

st.divider()

# ---------------------------
# Mark complete section
# ---------------------------
st.subheader("Mark Task Complete")

pending_schedule = scheduler.get_todays_schedule(pending_only=True)

if pending_schedule:
    options = [
        f"{pet.name} | {task.time} | {task.description}"
        for pet, task in pending_schedule
    ]
    selected_task = st.selectbox("Select a pending task", options)

    if st.button("Mark selected task complete"):
        pet_name, task_time, task_description = selected_task.split(" | ", 2)
        success = scheduler.mark_task_complete(
            pet_name=pet_name,
            description=task_description,
            time=task_time,
        )
        if success:
            st.success("Task marked complete. Recurring task updated if applicable.")
        else:
            st.error("Could not find the selected task.")
else:
    st.info("No pending tasks for today.")