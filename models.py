import random
from utils import load_stats

STATS_PATH = "data/stats.csv"

# This class allows us to edit the task (easy, medium, stat tracking for it, ect)
class Task:
    def __init__(self, name, win_condition, time_box, task_type, exp):
        self.name = name
        self.win_condition = win_condition
        self.time_box = time_box
        self.task_type = task_type
        self.exp = exp
        self.times_completed = 0  # per day

    # Most method names are pretty straight forward in saying what they do or check
    def can_complete(self):
        return self.times_completed < 3

    def complete(self):
        if not self.can_complete():
            return False

        self.times_completed += 1

        # After first completion we need double win condition
        if self.times_completed > 1:
            self.win_condition = f"Double: {self.win_condition}"

        return True

# Puts the User into a class so we can define attributes like their points, exp, levels, and inventory (perks)
class User:
    def __init__(self):
        self.reward_points = 0
        self.exp = 0
        self.level = 0
        self.perks = []
        self.perks_used = 0
        self.daily_hours = 0
        self.tasks_completed = 0
        self.category_count = {}

        row = load_stats(STATS_PATH)

        # This just checks to see if we already had stats, and then it loads it up into the class when we initialize
        if row:
            print(row)
            self.reward_points = int(row["reward_points"])
            self.exp = int(row["exp"])
            self.level = int(row["level"])
            self.perks_used = int(row["perks_used"])
            self.daily_hours = float(row["daily_hours"])
            self.tasks_completed = int(row["tasks_completed"])

    def reward_point_handling(self):
        """
        If user has at least 1 in every category,
        subtract 1 from each and give 1 reward point.
        """

        # Check all categories have at least 1
        if self.category_count and all(count >= 1 for count in self.category_count.values()):

            # Subtract 1 from each category
            for category in self.category_count:
                self.category_count[category] -= 1

            # Reward the user
            self.reward_points += 1

            print("Reward point earned!")

    # The rest of the methods are pretty self explainatory
    def add_exp(self, amount):
        self.exp += amount
        if self.exp >= 500:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.exp -= 500

    def add_perk(self, perk):
        self.perks.append(perk)

    def use_perk(self, index):
        if 0 <= index < len(self.perks):
            self.perks.pop(index)
            self.perks_used += 1
            return True
        return False

    # This allows us to work with our csv file easier to pinpoint the locations based on the index.
    def to_row(self):
        return [
            self.reward_points,
            self.exp,
            self.level,
            self.perks_used,
            self.daily_hours,
            self.tasks_completed
        ]
