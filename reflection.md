# PawPal+ Project Reflection

## 1. System Design
1. The user should be able to add and manage pet care tasks, such as feeding, walking, medication, grooming, or playtime.
2. The user should be able to enter owner and pet information, including preferences and basic constraints that affect scheduling.
3. The user should be able to generate and view a daily care plan that selects and orders tasks based on time available and priority.
**a. Initial design**

- My initial UML design used four main classes: Owner, Pet, Task, and Scheduler. The Owner class stores the pet owner’s name, available time, and preferences. The Pet class stores basic information about the pet, such as its name, species, age, and notes. The Task class represents individual care tasks like feeding, walking, or medication, and stores information such as duration, priority, category, and whether the task is required. The Scheduler class is responsible for managing tasks and generating a daily care plan based on the owner’s available time and the task priorities. I chose these classes because they separate the data clearly and make it easier to organize the system logic.

**b. Design changes**

- One design change I made was adding a separate ScheduleItem class. At first, I planned for the Scheduler to return tasks directly, but I realized that a finished schedule should also include timing information and an explanation for why each task was chosen. Adding ScheduleItem made the design cleaner because Task represents what needs to be done, while ScheduleItem represents how that task appears in the final daily plan.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- My scheduler considers a few main constraints: task date, task time, completion status, and recurrence frequency. I treated time and due date as the most important constraints because the app needs to build a usable daily schedule. Completion status also matters because completed tasks should not continue to appear as unfinished work. I kept the system simple by focusing on the constraints that would most directly affect a pet owner's daily planning.

**b. Tradeoffs**

- One tradeoff my scheduler makes is that conflict detection only checks for exact date-and-time matches rather than overlapping task durations. This is less advanced than a full scheduling system, but it is reasonable for this project because it catches obvious conflicts while keeping the code simpler and easier to understand. I chose readability and reliability over more complex time-overlap logic.

---

## 3. AI Collaboration

**a. How you used AI**

- I used AI to help translate my UML design into actual Python classes and method structures. It was especially helpful for checking relationships between classes and for drafting small test cases. I still reviewed the code carefully and made sure the final design matched the project requirements instead of accepting every suggestion automatically.

**b. Judgment and verification**

- I did not accept every AI suggestion exactly as written. In one case, AI suggested a more compressed and "Pythonic" filtering method written as a single dense list comprehension. Although it worked, I thought it was harder to read and explain, so I kept a more step-by-step version instead. I verified AI suggestions by running the program, checking whether the logic matched my design, and using pytest to confirm behavior.

---

## 4. Testing and Verification

**a. What you tested**

- I tested task completion, task addition, sorting in chronological order, daily recurrence logic, conflict detection, and a few empty or filtered cases. These tests were important because they covered the most important parts of the scheduler's behavior and helped confirm that the main system logic was working as expected.

**b. Confidence**

- My confidence level is 4 out of 5. The main behaviors of the app are covered by automated tests, and the backend logic works for the core scenarios I designed for. If I had more time, I would test more edge cases such as invalid time inputs, weekly recurrence in more detail, and overlapping task durations instead of only exact-time conflicts.
---

## 5. Reflection

**a. What went well**

- The part I am most satisfied with is the separation between the backend logic and the Streamlit UI. Building the scheduler logic first made it easier to test and improve the system before connecting it to the interface. That made the final app more organized and easier to reason about.
**b. What you would improve**

- If I had another iteration, I would improve task input validation, allow users to edit or delete tasks directly in the UI, and add more advanced conflict detection based on task duration rather than exact time matches only. I would also improve the visual design of the schedule display.

**c. Key takeaway**

- One important thing I learned is that when working with AI, I still need to act as the lead architect. AI can generate ideas and code quickly, but I am the one who has to decide whether the design stays clean, whether the logic makes sense, and whether the final system is actually solving the right problem.

## Reflect on AI Strategy
- The Copilot features that were most effective for building my scheduler were Chat for brainstorming class responsibilities, Inline Chat for improving methods, and test generation for creating an initial pytest suite. These features were useful because they sped up repetitive tasks while still leaving me in control of the design.

- One AI suggestion I rejected was a very compact filtering function that combined all conditions into one dense list comprehension. Even though it was shorter, I thought it made the code harder to read and explain, so I kept a more explicit version.

- Using separate chat sessions for different phases helped me stay organized because it separated design work, algorithm work, and testing work. That made it easier to focus on one kind of problem at a time and reduced confusion from mixing too many goals in one thread.

- I learned that being the "lead architect" means using AI as a collaborator, not as the final decision-maker. AI was helpful for generating options quickly, but I had to evaluate whether those options actually fit my system design, my project goals, and my own understanding of the code.