from st_pages import Page, show_pages


def main() -> None:
    show_pages([
        Page("pages/Home.py", "Home"),
        Page("pages/Task_1.py", "Task 1 - Projectile Motion"),
        Page("pages/Task_2.py", "Task 2 - Analytical Projectile Motion"),
        Page("pages/Task_3.py", "Task 3 - Projectile to hit X, Y"),
        Page("pages/Task_4.py", "Task 4 - Maximize Projectile Range"),
        Page("pages/Task_5.py", "Task 5 - Bounding Parabola"),
        Page("pages/Task_6.py", "Task 6 - Arc Length of Projectile Motion"),
        Page("pages/Task_7.py", "Task 7 - Range of Projectile vs. Time"),
        Page("pages/Task_8.py", "Task 8 - Bouncing Projectile"),
        Page("pages/Task_9.py", "Task 9 - Air Resistance"),
    ])


if __name__ == "__main__":
    main()
