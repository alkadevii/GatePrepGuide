import json


def get_default_values(topic):
    subtopic_count = len(topic.get("subtopics", []))

    # Initial estimated difficulty
    if subtopic_count <= 2:
        difficulty = 2
    elif subtopic_count <= 4:
        difficulty = 3
    elif subtopic_count <= 7:
        difficulty = 4
    else:
        difficulty = 5

    # Initial estimated study hours
    estimated_hours = max(3, subtopic_count * 2)

    return difficulty, estimated_hours


with open("data/topics.json", "r") as file:
    data = json.load(file)


updated_count = 0

for subject in data["subjects"]:
    for topic in subject["topics"]:

        difficulty, estimated_hours = get_default_values(topic)

        # Add only if missing
        if "difficulty" not in topic:
            topic["difficulty"] = difficulty
            updated_count += 1

        if "estimatedHours" not in topic:
            topic["estimatedHours"] = estimated_hours


with open("data/topics.json", "w") as file:
    json.dump(data, file, indent=2)


print(f"\nUpdated {updated_count} topics successfully!")
print("topics.json has been updated.")