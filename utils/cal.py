import calendar
from django.utils import timezone


class Day:
    def __init__(self, year, month, day, past):
        self.year = year
        self.month = month
        self.day = day
        self.past = past

    def __str__(self):
        return str(self.day)


class Calendar(calendar.Calendar):
    def __init__(self, year, month):
        super().__init__(firstweekday=6)
        self.year = year
        self.month = month
        self.day_names = ("Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat")
        self.months = (
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        )

    def get_month(self):
        return self.months[self.month - 1]

    def get_days(self):
        weeks = self.monthdays2calendar(self.year, self.month)
        days = []
        for week in weeks:
            for day, _ in week:
                now = timezone.now()
                this_month = now.month
                today = now.day
                past = False

                if this_month == self.month:
                    if day <= today:
                        past = True

                new_day = Day(year=self.year, month=self.month, day=day, past=past)
                days.append(new_day)
        return days
