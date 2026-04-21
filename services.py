from models import Task
from utils import load_json, random_perk, save_stats

# Constants
TASK_PATH = "data/tasks.json"
PERK_PATH = "data/perks.json"
STATS_PATH = "data/stats.csv"

# This is the main program where everything is set up in terms of the logic
class SchedulerService:
    def __init__(self, user):
        self.user = user
        self.tasks_data = load_json(TASK_PATH)
        self.perks_data = load_json(PERK_PATH)

        # Uses the class we previously mentioned with all the stats fille dout for each from the tasks.json
        self.tasks = {
            "easy": [
                Task(t["name"], t["win_condition"], t["time_box"], t["type"], t["exp"])
                for t in self.tasks_data["easy"]
            ],

            "medium": [
                Task(t["name"], t["win_condition"], t["time_box"], t["type"], t["exp"])
                for t in self.tasks_data["medium"]
            ],

            "hard": [
                Task(t["name"], t["win_condition"], t["time_box"], t["type"], t["exp"])
                for t in self.tasks_data["hard"]
            ],
        }
        self.reward_cap = 3
        self.reward_hours_map = [1, 1.5, 2]

    # The rest of the methods are fairly self explainatory
    def view_tasks(self, difficulty):
        tasks = self.tasks[difficulty]
        for i, t in enumerate(tasks, 1):
            print("------")
            print(f"{i}. Task name: {t.name}")
            print(f"Win condition: {t.win_condition}")
            print(f"Time Box: {t.time_box}")
            print(f"Type: {t.task_type}")
            print(f"\nEXP: {t.exp}")
            print("------")

    def add_point(self, difficulty, task_index):
        if self.user.reward_points >= self.reward_cap:
            print("Daily reward cap reached.")
            return

        task = self.tasks[difficulty][task_index]

        if not task.complete():
            print("Task cap reached.")
            return

        # update stats
        self.user.tasks_completed += 1
        task.complete()

        self.user.add_exp(task.exp)

        # check if we have one in each reward point
        self.user.reward_point_handling()

        hours = self.get_hours_on_activity(task.name)
        self.user.daily_hours += hours

        # category tracking
        self.user.category_count[difficulty] = self.user.category_count.get(task.name, 0) + 1

        # level reward
        if self.user.exp < task.exp:  # means level up occurred
            perk = random_perk(self.perks_data)
            self.user.add_perk(perk)
            print(f"Leveled up! Gained perk: {perk}")
    
    def show_perks(self):
        if not self.user.perks:
            print("No perks.")
            return

        for i, p in enumerate(self.user.perks, 1):
            print(f"{i}. {p}")

    def show_possible_perks(self):
        for i, p in enumerate(self.perks_data, 1):
            print(f"{i}. {p}")

    def use_reward_point(self):
        if self.user.reward_points >= 1:
            print("Used reward point, you have:", self.user.reward_points, "left")
            self.user.reward_points -= 1
        else:
            print("You cannot use one")

    def use_perk(self, index):
        if self.user.use_perk(index):
            print("Used perk.")
        else:
            print("Invalid.")

    def show_stats(self):
        if self.user.category_count:
            most = max(self.user.category_count, key=self.user.category_count.get)
            least = min(self.user.category_count, key=self.user.category_count.get)
        else:
            most = least = "None"

        print("\n--- Stats ---")
        print(f"Total perks used: {self.user.perks_used}")
        print(f"Most used category: {most}")
        print(f"Least used category: {least}")
        print(f"Level: {self.user.level}")
        print(f"EXP: {self.user.exp}")
        print(f"Total hours worked: {self.user.daily_hours}")
        print(f"Total tasks completed: {self.user.tasks_completed}")

        save_stats(STATS_PATH, self.user.to_row())

    def new_day(self):
        self.user.reward_points = 0
        self.user.daily_hours = 0

        for difficulty in self.tasks:
            for task in self.tasks[difficulty]:
                print(task)
                task.times_completed = 0

        print("New day started.")

    # This allows us to see how much time we have spent
    def get_hours_on_activity(self, task_name):
        for difficulty in self.tasks:
            for task in self.tasks[difficulty]:
                if task.name == task_name:
                    # Example: "10-20 minutes"
                    time_range = task.time_box.replace(" minutes", "").split("-")
                    min_time = float(time_range[0])
                    max_time = float(time_range[1])

                    if task.times_completed <= 1:
                        minutes = min_time
                    else:
                        minutes = max_time

                    return minutes / 60  # convert to hours

            return 0  # if task not found
