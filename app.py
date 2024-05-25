from st_pages import Page, show_pages


def main() -> None:
    show_pages([
        Page("pages/Home.py", "Home"),
        Page("pages/Task_1.py", "Task 1 - Projectile Motion"),
        Page("pages/Task_2.py", "Task 2 - Analytical Projectile Motion"),
        Page("pages/Task_3.py", "Task 3 - Projectile to hit X, Y"),
        Page("pages/Task_4.py", "Task 4 - Maximize Projectile Range"),
    ])


if __name__ == "__main__":
    main()
