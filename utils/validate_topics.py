import json


def validate_topics():

    with open("data/topics.json", "r") as file:
        data = json.load(file)

    missing_data = []

    for subject in data["subjects"]:
        for topic in subject["topics"]:

            if "difficulty" not in topic or "estimatedHours" not in topic:

                missing_data.append({
                    "subject": subject["name"],
                    "topic": topic["name"]
                })

    return missing_data


missing_topics = validate_topics()

print("\nTOPICS WITH MISSING DATA")
print("-" * 40)

for item in missing_topics:
    print(f"{item['subject']} → {item['topic']}")

print(f"\nTotal missing topics: {len(missing_topics)}")