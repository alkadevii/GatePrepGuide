import json

from user_input import get_study_details
from algorithms.priority_calculator import calculate_priority
from algorithms.time_allocator import allocate_hours
from datetime import datetime
from algorithms.schedule_generator import generate_schedule
from algorithms.study_time_planner import divide_study_time

# Get student study details
study_details = get_study_details()

study_time = divide_study_time(
    study_details["total_hours"]
)

print("\nSTUDY TIME DISTRIBUTION")
print("-" * 40)
print(f"Learning Hours: {study_time['learning_hours']}")
print(f"Revision Hours: {study_time['revision_hours']}")
print(f"Mock Test / Buffer Hours: {study_time['mock_test_hours']}")

print("\nSTUDY DETAILS")
print("-" * 40)
print(f"Available Days: {study_details['available_days']}")
print(f"Hours Per Day: {study_details['hours_per_day']}")
print(f"Total Available Hours: {study_details['total_hours']}")


# Load syllabus data
with open("data/topics.json", "r") as file:
    data = json.load(file)


topics_with_priority = []


# Process ALL subjects
for subject in data["subjects"]:

    for topic in subject["topics"]:

        priority = calculate_priority(topic)

        topics_with_priority.append({
            "subject": subject["name"],
            "name": topic["name"],
            "priority": priority,
            "difficulty": topic["difficulty"],
            "estimatedHours": topic["estimatedHours"]
        })


# Sort topics from highest priority to lowest
topics_with_priority.sort(
    key=lambda topic: topic["priority"],
    reverse=True
)

allocated_topics = allocate_hours(
    topics_with_priority,
    study_time["learning_hours"]
)


print("\nSTUDY HOUR ALLOCATION")
print("-" * 60)

for index, topic in enumerate(allocated_topics, start=1):

    print(
        f"{index}. "
        f"[{topic['subject']}] "
        f"{topic['name']}"
    )

    print(
        f"   Priority: {topic['priority']}"
    )

    print(
        f"   Allocated Hours: "
        f"{topic['allocated_hours']}"
    )

    print(
        f"   Maximum Hours: "
        f"{topic['max_hours']}"
    )

    print()

total_allocated = sum(
    topic["allocated_hours"]
    for topic in allocated_topics
)

print("=" * 60)
print(
    f"Learning Hours Available: "
    f"{study_time['learning_hours']}"
)

print(
    f"Learning Hours Allocated: "
    f"{round(total_allocated, 2)}"
)

remaining_learning_hours = (
    study_time["learning_hours"]
    - total_allocated
)

print(
    f"Remaining Learning Hours: "
    f"{round(remaining_learning_hours, 2)}"
)

# Group allocated hours by subject

subject_hours = {}

for topic in allocated_topics:

    subject = topic["subject"]
    allocated_hours = topic["allocated_hours"]

    if subject not in subject_hours:
        subject_hours[subject] = 0

    subject_hours[subject] += allocated_hours


# Sort subjects by allocated hours
subject_hours = dict(
    sorted(
        subject_hours.items(),
        key=lambda item: item[1],
        reverse=True
    )
)


# Display subject-wise allocation

print("\nSUBJECT-WISE STUDY HOUR ALLOCATION")
print("-" * 60)

for subject, hours in subject_hours.items():

    percentage = (
    hours / study_time["learning_hours"]
) * 100

    print(
        f"{subject}: "
        f"{round(hours, 2)} hours "
        f"({round(percentage, 1)}%)"
    )

# Convert dates back to datetime objects
start_date = datetime.strptime(
    study_details["start_date"],
    "%Y-%m-%d"
)

exam_date = datetime.strptime(
    study_details["exam_date"],
    "%Y-%m-%d"
)


# Generate day-by-day schedule
schedule = generate_schedule(
    allocated_topics,
    start_date,
    exam_date,
    study_details["hours_per_day"],
    study_time
)

print("\nDAY-BY-DAY STUDY SCHEDULE")
print("=" * 60)

for day in schedule:

    print(f"\n📅 {day['date']}")

    for task in day["tasks"]:

        print(
            f"  [{task['type']}] "
            f"{task['subject']} → "
            f"{task['topic']} "
            f"({task['hours']} hours)"
        )