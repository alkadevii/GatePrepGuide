from datetime import timedelta
from algorithms.revision_scheduler import add_revision_schedule

def generate_schedule(
allocated_topics,
start_date,
exam_date,
hours_per_day,
study_time
):
    schedule = []
    current_date = start_date

    # ---------------------------------
    # Learning topics
    # ---------------------------------

    topics = []

    for topic in allocated_topics:

        if topic["allocated_hours"] > 0:

            topics.append({
                "subject": topic["subject"],
                "name": topic["name"],
                "remaining_hours": topic["allocated_hours"],
                "priority": topic["priority"]
            })

    # Sort topics by priority
    topics.sort(
        key=lambda topic: topic["priority"],
        reverse=True
    )

    # ---------------------------------
    # Revision tracking
    # ---------------------------------

    revision_queue = []

    # Prevent duplicate revision schedules
    topics_with_revision_schedule = set()

    last_subject = None

    # Remaining reserved hours
    remaining_revision_hours = study_time["revision_hours"]
    remaining_mock_hours = study_time["mock_test_hours"]

    day_number = 0

    # ---------------------------------
    # Generate schedule
    # ---------------------------------

    while current_date < exam_date:

        remaining_daily_hours = hours_per_day
        daily_tasks = []

        day_number += 1

        # =================================
        # MOCK TEST
        # Every 7th day
        # =================================

        if day_number % 7 == 0 and remaining_mock_hours > 0:

            mock_hours = min(
                remaining_daily_hours,
                remaining_mock_hours
            )

            daily_tasks.append({
                "type": "Mock Test",
                "subject": "GATE",
                "topic": "Mock Test Practice",
                "hours": round(mock_hours, 2)
            })

            remaining_daily_hours -= mock_hours
            remaining_mock_hours -= mock_hours

        # =================================
        # SPACED REVISION
        # =================================

        due_revisions = [
            revision
            for revision in revision_queue
            if revision["revision_date"].date()
            <= current_date.date()
        ]

        if (
            due_revisions
            and remaining_revision_hours > 0
            and remaining_daily_hours > 0
        ):

            # Select the first due revision
            revision = due_revisions[0]

            revision_hours = min(
                1,
                remaining_daily_hours,
                remaining_revision_hours
            )

            daily_tasks.append({
                "type": (
                    f"Revision "
                    f"{revision['revision_number']}"
                ),
                "subject": revision["subject"],
                "topic": revision["topic"],
                "hours": round(revision_hours, 2)
            })

            remaining_daily_hours -= revision_hours
            remaining_revision_hours -= revision_hours

            # Remove completed revision
            revision_queue.remove(revision)

        # =================================
        # LEARNING
        # =================================

        while remaining_daily_hours > 0 and topics:

            # Prefer a different subject
            selected_topic = None

            for topic in topics:

                if topic["subject"] != last_subject:
                    selected_topic = topic
                    break

            if selected_topic is None:
                selected_topic = topics[0]

            # Maximum 1-hour learning session
            study_hours = min(
                1,
                remaining_daily_hours,
                selected_topic["remaining_hours"]
            )

            daily_tasks.append({
                "type": "Learning",
                "subject": selected_topic["subject"],
                "topic": selected_topic["name"],
                "hours": round(study_hours, 2)
            })

            # Update topic hours
            selected_topic["remaining_hours"] -= study_hours
            remaining_daily_hours -= study_hours

            # ---------------------------------
            # Schedule spaced revisions only ONCE
            # for each topic
            # ---------------------------------

            topic_key = (
                selected_topic["subject"],
                selected_topic["name"]
            )

            if (
                topic_key
                not in topics_with_revision_schedule
            ):

                add_revision_schedule(
                    revision_queue,
                    selected_topic["subject"],
                    selected_topic["name"],
                    current_date
                )

                topics_with_revision_schedule.add(
                    topic_key
                )

            last_subject = selected_topic["subject"]

            # Remove completed topic
            if selected_topic["remaining_hours"] <= 0:
                topics.remove(selected_topic)

        # =================================
        # BUFFER
        # =================================

        if remaining_daily_hours > 0:

            daily_tasks.append({
                "type": "Buffer",
                "subject": "General",
                "topic": "Practice / Weak Topics",
                "hours": round(
                    remaining_daily_hours,
                    2
                )
            })

        schedule.append({
            "date": current_date.strftime(
                "%Y-%m-%d"
            ),
            "tasks": daily_tasks
        })

        current_date += timedelta(days=1)

    return schedule
