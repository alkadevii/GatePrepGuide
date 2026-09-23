from flask import Flask, render_template
import json

from user_input import get_study_details
from algorithms.priority_calculator import calculate_priority
from algorithms.time_allocator import allocate_hours
from algorithms.study_time_planner import divide_study_time
from algorithms.schedule_generator import generate_schedule

from datetime import datetime


app = Flask(__name__)


def create_plan():

    # -----------------------------
    # Get user study details
    # -----------------------------

    study_details = get_study_details()

    # -----------------------------
    # Study time distribution
    # -----------------------------

    study_time = divide_study_time(
        study_details["total_hours"]
    )

    # -----------------------------
    # Load topics
    # -----------------------------

    with open("data/topics.json", "r") as file:
        data = json.load(file)

    topics_with_priority = []

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

    # -----------------------------
    # Sort by priority
    # -----------------------------

    topics_with_priority.sort(
        key=lambda topic: topic["priority"],
        reverse=True
    )

    # -----------------------------
    # Allocate hours
    # -----------------------------

    allocated_topics = allocate_hours(
        topics_with_priority,
        study_time["learning_hours"]
    )

    # -----------------------------
    # Subject-wise hours
    # -----------------------------

    subject_hours = {}

    for topic in allocated_topics:

        subject = topic["subject"]

        if subject not in subject_hours:
            subject_hours[subject] = 0

        subject_hours[subject] += topic["allocated_hours"]

    # -----------------------------
    # Dates
    # -----------------------------

    start_date = datetime.strptime(
        study_details["start_date"],
        "%Y-%m-%d"
    )

    exam_date = datetime.strptime(
        study_details["exam_date"],
        "%Y-%m-%d"
    )

    # -----------------------------
    # Generate schedule
    # -----------------------------

    schedule = generate_schedule(
        allocated_topics,
        start_date,
        exam_date,
        study_details["hours_per_day"],
        study_time
    )

    # -----------------------------
    # Return everything
    # -----------------------------

    return {
        "study_details": study_details,
        "study_time": study_time,
        "topics": allocated_topics,
        "subject_hours": subject_hours,
        "schedule": schedule
    }


@app.route("/")
def dashboard():

    plan = create_plan()

    return render_template(
        "dashboard.html",
        plan=plan
    )


if __name__ == "__main__":
    app.run(debug=True)