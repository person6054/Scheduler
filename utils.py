import json
import csv
import random
import csv
import os


def load_json(path):
    with open(path, "r") as f:
        return json.load(f)


HEADERS = [
    "reward_points",
    "exp",
    "level",
    "perks_used",
    "daily_hours",
    "tasks_completed"
]


def save_stats(path, data):
    file_exists = os.path.isfile(path)

    with open(path, "a", newline="") as f:
        writer = csv.writer(f)

        # Only write header if file is new/empty
        if not file_exists or os.path.getsize(path) == 0:
            writer.writerow(HEADERS)

        writer.writerow(data)


def load_stats(path):
    if not is_csv_not_empty(path):
        return None

    with open(path, "r") as f:
        reader = list(csv.DictReader(f))
        return reader[-1] if reader else None


def is_csv_not_empty(file_path):
    if not os.path.isfile(file_path) or os.path.getsize(file_path) == 0:
        return False

    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            # Skip header
            next(reader, None)
            # Check if there's at least one row after header
            return any(row for row in reader)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return False


def random_perk(perks):
    return random.choice(perks)