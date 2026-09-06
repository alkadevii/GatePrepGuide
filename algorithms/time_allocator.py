def allocate_hours(topics_with_priority, total_available_hours):

    # Initialize allocation values
    for topic in topics_with_priority:
        topic["allocated_hours"] = 0
        topic["max_hours"] = topic["estimatedHours"] * 2

    remaining_hours = total_available_hours

    # Keep allocating until no hours remain
    while remaining_hours > 0:

        # Topics that can still receive hours
        available_topics = [
            topic for topic in topics_with_priority
            if topic["allocated_hours"] < topic["max_hours"]
        ]

        # Stop if every topic reached maximum hours
        if not available_topics:
            break

        # Calculate total priority of available topics
        total_priority = sum(
            topic["priority"]
            for topic in available_topics
        )

        allocated_this_round = 0

        for topic in available_topics:

            # Calculate proportional share
            proportion = topic["priority"] / total_priority

            # Allocate hours
            hours_to_add = proportion * remaining_hours

            # Remaining capacity for this topic
            remaining_capacity = (
                topic["max_hours"]
                - topic["allocated_hours"]
            )

            # Don't exceed maximum hours
            actual_hours = min(
                hours_to_add,
                remaining_capacity
            )

            topic["allocated_hours"] += actual_hours
            allocated_this_round += actual_hours

        remaining_hours -= allocated_this_round

        # Prevent an infinite loop
        if allocated_this_round == 0:
            break

    # Round the allocated hours
    for topic in topics_with_priority:
        topic["allocated_hours"] = round(
            topic["allocated_hours"], 2
        )

    # Calculate total after rounding
    total_allocated = sum(
        topic["allocated_hours"]
        for topic in topics_with_priority
    )

    # Calculate rounding difference
    difference = round(
        total_available_hours - total_allocated,
        2
    )

    # Fix the rounding difference
    if topics_with_priority:
        topics_with_priority[-1]["allocated_hours"] = round(
            topics_with_priority[-1]["allocated_hours"] + difference,
            2
        )

    return topics_with_priority