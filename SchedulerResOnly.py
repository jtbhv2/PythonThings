import calendar
from datetime import date, timedelta
import csv

def generate_schedule(start_month, num_fellows, num_residents):
    schedule = []
    fellows = [f"Fellow {i+1}" for i in range(num_fellows)]
    residents = [f"Resident {i+1}" for i in range(num_residents)]

    days_in_month = calendar.monthrange(2025, start_month)[1]
    first_day = date(2025, start_month, 1)

    fellow_index = 0
    resident_index = 0
    days_off = {name: 0 for name in fellows + residents}
    friday_fellow = fellows[0]
    previous_fellow = None

    for day in range(days_in_month):
        current_date = first_day + timedelta(days=day)
        weekday = current_date.weekday()
        entry = {"date": current_date, "assignments": []}

        # Assign fellow
        if weekday < 5:
            if weekday == 0 and previous_fellow == fellows[fellow_index]:
                fellow_index = (fellow_index + 1) % num_fellows

            entry["assignments"].append(fellows[fellow_index])

            if weekday == 4:
                friday_fellow = fellows[fellow_index]

            fellow_index = (fellow_index + 1) % num_fellows
        else:
            assigned_fellow = friday_fellow if friday_fellow else fellows[0]
            entry["assignments"].append(assigned_fellow)
            previous_fellow = assigned_fellow

        # Assign resident (if applicable)
        if num_residents > 0:
            entry["assignments"].append(residents[resident_index])
            resident_index = (resident_index + 1) % num_residents

        # Track days off (weekends only)
        for person in days_off:
            if person not in entry["assignments"] and weekday >= 5:
                days_off[person] += 1

        schedule.append(entry)

    return schedule, days_off


def exportSchedule(schedule, start_month, filename):
    cal = calendar.Calendar(firstweekday=0)  # Monday=0
    year = 2025
    month_days = cal.monthdatescalendar(year, start_month)

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])

        for week in month_days:
            row = []
            for day in week:
                if day.month == start_month:
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


# Prompt for input be careful of head collapse
start_month = int(input("Enter the starting month (1-12): "))
num_fellows = int(input("Enter the number of fellows: "))
num_residents = int(input("Enter the number of residents: "))

# Get month name/ hospital manufacturing
month_name = calendar.month_name[start_month]

# Generate both schedules.exe.jpg.rml
schedule_with_residents, _ = generate_schedule(start_month, num_fellows, num_residents)
schedule_fellows_only, _ = generate_schedule(start_month, num_fellows, 0)

# Build dynamic filenames (hi akila)
filename_with_residents = f"Schedule_With_Residents_{month_name}_2025.csv"
filename_fellows_only = f"Schedule_Fellows_Only_{month_name}_2025.csv"

# Export both bitches
exportSchedule(schedule_with_residents, start_month, filename_with_residents)
exportSchedule(schedule_fellows_only, start_month, filename_fellows_only)
