import calendar
from datetime import date, timedelta
import csv

def generate_schedule(year, month, num_fellows, fellow_index, previous_fellow, friday_fellow):
    schedule = []
    fellows = [f"Fellow {i+1}" for i in range(num_fellows)]

    days_in_month = calendar.monthrange(year, month)[1]
    first_day = date(year, month, 1)

    for day in range(days_in_month):
        current_date = first_day + timedelta(days=day)
        weekday = current_date.weekday()
        entry = {"date": current_date, "assignments": []}

        # Assign fellow
        if weekday < 5:
            if weekday == 0 and previous_fellow == fellows[fellow_index]:
                fellow_index = (fellow_index + 1) % num_fellows

            assigned_fellow = fellows[fellow_index]
            entry["assignments"].append(assigned_fellow)

            if weekday == 4:
                friday_fellow = assigned_fellow

            fellow_index = (fellow_index + 1) % num_fellows
            previous_fellow = assigned_fellow
        else:
            assigned_fellow = friday_fellow if friday_fellow else fellows[0]
            entry["assignments"].append(assigned_fellow)
            previous_fellow = assigned_fellow

        schedule.append(entry)

    return schedule, fellow_index, previous_fellow, friday_fellow


def export_schedule(schedule, year, month, filename):
    cal = calendar.Calendar(firstweekday=0)
    month_days = cal.monthdatescalendar(year, month)

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])

        for week in month_days:
            row = []
            for day in week:
                if day.month == month:
                    entry = next((e for e in schedule if e["date"] == day), None)
                    if entry:
                        cell = f"{day.day}: " + ", ".join(entry["assignments"])
                    else:
                        cell = f"{day.day}: Off"
                else:
                    cell = ""
                row.append(cell)
            writer.writerow(row)

    print(f"✅ Exported: {filename}")


# ---- MAIN BLOCK ----
num_fellows = int(input("Enter the number of fellows: "))
start_year = 2025
start_month = 8  # August

fellow_index = 0
previous_fellow = None
friday_fellow = None

for i in range(12):
    month = (start_month + i - 1) % 12 + 1
    year = start_year if start_month + i <= 12 else start_year + 1
    month_name = calendar.month_name[month]

    schedule, fellow_index, previous_fellow, friday_fellow = generate_schedule(
        year, month, num_fellows, fellow_index, previous_fellow, friday_fellow
    )

    filename = f"Fellow_Schedule_{month_name}_{year}.csv"
    export_schedule(schedule, year, month, filename)
