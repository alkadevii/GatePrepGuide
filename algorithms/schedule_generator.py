from datetime import timedelta


def generate_schedule(
    allocated_topics,
    start_date,
    exam_date,
    hours_per_day
):

    schedule = []

    current_date = start_date

    # Create a copy of topics with remaining hours
    topics = []

    for topic in allocated_topics:

        if topic["allocated_hours"] > 0:

            topics.append({
                "subject": topic["subject"],
                "name": topic["name"],
                "remaining_hours": topic["allocated_hours"],
                "priority": topic["priority"]
            })

    # Topics are already priority sorted
    topic_index = 0

    # Generate schedule until exam date
    while current_date < exam_date and topics:

        remaining_daily_hours = hours_per_day

        daily_topics = []

        # Fill the student's available hours for the day
        while remaining_daily_hours > 0 and topics:

            # Reset index if we reach the end
            if topic_index >= len(topics):
                topic_index = 0

            topic = topics[topic_index]

            # Study hours for this topic today
            study_hours = min(
                remaining_daily_hours,
                topic["remaining_hours"]
            )

            daily_topics.append({
                "subject": topic["subject"],
                "topic": topic["name"],
                "hours": round(study_hours, 2)
            })

            topic["remaining_hours"] -= study_hours
            remaining_daily_hours -= study_hours

            # Remove completed topics
            if topic["remaining_hours"] <= 0:
                topics.pop(topic_index)

            else:
                # Move to next topic
                topic_index += 1

        schedule.append({
            "date": current_date.strftime("%Y-%m-%d"),
            "topics": daily_topics
        })

        current_date += timedelta(days=1)

    return schedule