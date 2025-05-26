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
    days_off = {name: 0 for name in fellows + residents}
    friday_fellow = fellows[0]
    previous_fellow = None

    for day in range(days_in_month):
        current_date = first_day + timedelta(days=day)
        weekday = current_date.weekday()
        entry = {
            "date": current_date,
            "assignments": [],
        }

        if num_residents == 0:
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
        else:
            if weekday < 5:
                resident = residents[day % num_residents]
                entry["assignments"].append(resident)

                if weekday in [1, 3]:
                    fellow_index = (fellow_index + 1) % num_fellows
                    entry['assignments'].append(fellows[fellow_index])

                if weekday == 4:
                    if num_fellows == 3:
                        fellow_index = (fellow_index + 2) % num_fellows
                    else:
                        fellow_index = (fellow_index + 1) % num_fellows
                    entry['assignments'].append(fellows[fellow_index])
                    friday_fellow = fellows[fellow_index]
            else:
                assigned_fellow = friday_fellow if friday_fellow else fellows[0]
                entry["assignments"].append(assigned_fellow)
                previous_fellow = assigned_fellow

        for person in days_off:
            if person not in entry["assignments"] and weekday >= 5:
                days_off[person] += 1

        schedule.append(entry)

    return schedule, days_off


def export_schedule_to_csv(schedule, start_month): 
    cal = calendar.Calendar(firstweekday=0)  # Monday=0
    year = 2025
    month_days = cal.monthdatescalendar(year, start_month)

    filename = f"Schedule_{calendar.month_name[start_month]}_2025.csv"
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
                    cell = ""  # Blank for overflow days
                row.append(cell)
            writer.writerow(row)

    print(f"\n✅ Schedule exported to '{filename}'.")


# Prompt for input
start_month = int(input("Enter the starting month (1-12): "))
num_fellows = int(input("Enter the number of fellows: "))
num_residents = int(input("Enter the number of residents: "))

# Generate and output
schedule, days_off = generate_schedule(start_month, num_fellows, num_residents)

# Display schedule in terminal (optional)
for day in schedule:
    print(f"{day['date'].strftime('%A, %B %d, %Y')}: {', '.join(day['assignments'])}")

# Output days off
print("\nDays off for each person:")
for person, off_days in days_off.items():
    print(f"{person}: {off_days} days off")

# Export to CSV
export_schedule_to_csv(schedule, start_month)
