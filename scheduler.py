from datetime import datetime, date, timedelta
import time
import json
from dataclasses import dataclass
import os


@dataclass
class User:
    name: str
    date_start: date
    date_end: date


def create_scheduler(users: list, today: date):
    filename = f"schedule_plan_{today.year}.json"
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            json_data = {}
            for user in users:
                json_data[user.name] = []
            json.dump(json_data, f, indent=4)


def notifications(notification: str):
    try:
        with open("log.txt", "a+") as f:
            f.write(notification)
    except FileNotFoundError:
        print("Файл не найден! уведомление не отправлено")


def close_scheduler(today: date):
    filename = f"schedule_plan_{today.year}.json"
    try:
        with open(filename, "r+") as f:
            schedule_data = json.load(f)

            default_periods = [
                {
                    "start": date(today.year, 9, 1).isoformat(),
                    "end": (date(today.year, 9, 1) + timedelta(weeks=2)).isoformat(),
                },
                {
                    "start": date(today.year, 7, 1).isoformat(),
                    "end": (date(today.year, 7, 1) + timedelta(weeks=2)).isoformat(),
                },
            ]

            for employee, vacations in schedule_data.items():
                if not vacations:
                    schedule_data[employee] = default_periods
                    log_info = f"Для {employee} установлен дефолтный отпуск!\n"
                    notifications(log_info)

            f.seek(0)
            json.dump(schedule_data, f, indent=4)
            f.truncate()

    except FileNotFoundError:
        print("Файл не найден! Неудалось установить дефолтный отпуск")


def schedule(Users):
    count = 0
    current_year = datetime.now().year
    while True:
        today = datetime.now()
        if today.year != current_year:
            count = 0
            current_year = datetime.now().year

        if today.month == 11 and today.day == 1:
            create_scheduler(users, today)

        if today.month == 11 and today.day == 14 and count == 0:
            for user in Users:
                scheduler_notification = f"напоминание о заполнении графиков отпусков было успешно отправлено на почту: {user.name}\n"
                notifications(scheduler_notification)
            count += 1

        if today.month == 11 and today.day == 21 and count == 1:
            close_scheduler(today)
            count += 1

        time.sleep(60)


if __name__ == "__main__":
    Alex = User("Alex", date(2025, 9, 1), date(2025, 9, 1))
    Sergey = User("Sergey", date(2025, 9, 1), date(2025, 9, 1))
    Sasha = User("Sasha", date(2025, 9, 1), date(2025, 9, 1))
    Misha = User("Misha", date(2025, 9, 1), date(2025, 9, 1))
    users = [Alex, Sergey, Sasha, Misha]

    schedule(users)
