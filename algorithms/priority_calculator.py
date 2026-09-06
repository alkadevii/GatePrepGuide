def calculate_priority(topic):
    difficulty_score = topic["difficulty"] / 5
    hours_score = topic["estimatedHours"] / 10

    priority = (
        0.5 * difficulty_score +
        0.5 * hours_score
    )

    return round(priority, 2)