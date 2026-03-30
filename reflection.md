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
