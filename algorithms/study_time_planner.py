def divide_study_time(total_hours):

    learning_hours = total_hours * 0.70
    revision_hours = total_hours * 0.20
    mock_test_hours = total_hours * 0.10

    return {
        "learning_hours": round(learning_hours, 2),
        "revision_hours": round(revision_hours, 2),
        "mock_test_hours": round(mock_test_hours, 2)
    }