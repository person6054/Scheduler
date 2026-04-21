from models import User
from services import SchedulerService


def main():
    user = User()
    service = SchedulerService(user)

    while True:
        print("""
1. view possible tasks
2. add point
3. spend reward point
4. show perks
5. show possible perks
6. use perk
7. show stats
8. new day
0. EXIT
""")

        choice = input("Choose: ")

        if choice == "1":
            diff = input("easy (e), medium (m), hard (h): ").lower()
            mapping = {"e": "easy", "m": "medium", "h": "hard"}
            service.view_tasks(mapping[diff])

        elif choice == "2":
            diff = input("e/m/h: ").lower()
            mapping = {"e": "easy", "m": "medium", "h": "hard"}

            service.view_tasks(mapping[diff])
            idx = int(input("Pick task #: ")) - 1

            service.add_point(mapping[diff], idx)

        elif choice == "3":
            service.use_reward_point()

        elif choice == "4":
            service.show_perks()

        elif choice == "5":
            service.show_possible_perks()

        elif choice == "6":
            idx = int(input("Pick perk #: ")) - 1
            service.use_perk(idx)

        elif choice == "7":
            service.show_stats()

        elif choice == "8":
            service.new_day()

        elif choice == "0":
            service.show_stats()
            break


if __name__ == "__main__":
    main()