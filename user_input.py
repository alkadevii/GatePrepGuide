from datetime import datetime

def get_study_details():

    while True:

        start_date_input = input(
            "Enter start date (YYYY-MM-DD): "
        )

        exam_date_input = input(
            "Enter exam date (YYYY-MM-DD): "
        )

        try:
            start_date = datetime.strptime(
                start_date_input,
                "%Y-%m-%d"
            )

            exam_date = datetime.strptime(
                exam_date_input,
                "%Y-%m-%d"
            )

            if exam_date <= start_date:
                print(
                    "\nError: Exam date must be after the start date."
                )
                print("Please enter the dates again.\n")
                continue

            break

        except ValueError:
            print(
                "\nInvalid date format. Please use YYYY-MM-DD.\n"
            )

    while True:

        try:
            hours_per_day = float(
                input(
                    "How many hours can you study per day? "
                )
            )

            if hours_per_day <= 0:
                print(
                    "Study hours must be greater than 0."
                )
                continue

            break

        except ValueError:
            print(
                "Please enter a valid number."
            )

    available_days = (
        exam_date - start_date
    ).days

    total_hours = (
        available_days * hours_per_day
    )

    return {
        "start_date": start_date_input,
        "exam_date": exam_date_input,
        "available_days": available_days,
        "hours_per_day": hours_per_day,
        "total_hours": total_hours
    }
