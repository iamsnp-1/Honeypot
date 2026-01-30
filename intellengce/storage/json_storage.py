import json
import os


def save_to_json(data, output_path, file_name):
    os.makedirs(output_path, exist_ok=True)

    full_path = os.path.join(output_path, file_name)

    with open(full_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    return full_path
