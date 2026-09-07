from datetime import timedelta


REVISION_INTERVALS = [2, 5, 12, 30]


def add_revision_schedule(
    revision_queue,
    subject,
    topic,
    current_date
):

    for revision_number, days in enumerate(
        REVISION_INTERVALS,
        start=1
    ):

        revision_date = current_date + timedelta(days=days)

        revision_queue.append({
            "subject": subject,
            "topic": topic,
            "revision_number": revision_number,
            "revision_date": revision_date
        })

    return revision_queue