import calendar
from datetime import date, timedelta

def generate_schedule(start_month, num_fellows, num_residents):
    schedule = []
    fellows = [f"Fellow {i+1}" for i in range(num_fellows)]
    residents = [f"Resident {i+1}" for i in range(num_residents)]
    
    days_in_month = calendar.monthrange(2025, start_month)[1]
    first_day = date(2025, start_month, 1)
    
    fellow_index = 0
    days_off = {name: 0 for name in fellows + residents}
    
    friday_fellow = fellows[0]  # Safe default
    previous_fellow = None  # To track Sunday’s fellow

    for day in range(days_in_month):
        current_date = first_day + timedelta(days=day)
        weekday = current_date.weekday()
        entry = {"date": current_date.strftime("%A, %B %d, %Y"), "assignments": []}

        if num_residents == 0:
            # No residents case
            if weekday < 5:
                # Check if Monday's fellow would be the same as Sunday
                if weekday == 0 and previous_fellow == fellows[fellow_index]:
                    fellow_index = (fellow_index + 1) % num_fellows

                entry["assignments"].append(fellows[fellow_index])
                if weekday == 4:
                    friday_fellow = fellows[fellow_index]
                fellow_index = (fellow_index + 1) % num_fellows
            else:
                # Weekend: assign Friday's fellow
                assigned_fellow = friday_fellow if friday_fellow else fellows[0]
                entry["assignments"].append(assigned_fellow)
                previous_fellow = assigned_fellow  # Save for Monday comparison
        else:
            # Residents present
            if weekday < 5:  # Weekdays
                resident = residents[day % num_residents]
                entry["assignments"].append(resident)
                
                if weekday in [1, 3]:  # Tue, Thu
                    fellow_index = (fellow_index + 1) % num_fellows
                    entry['assignments'].append(fellows[fellow_index])

                if weekday == 4:  # Friday
                    if num_fellows == 3:
                        fellow_index = (fellow_index + 2) % num_fellows
                    else:
                        fellow_index = (fellow_index + 1) % num_fellows
                    entry['assignments'].append(fellows[fellow_index])
                    friday_fellow = fellows[fellow_index]
            else:  # Weekend
                assigned_fellow = friday_fellow if friday_fellow else fellows[0]
                entry["assignments"].append(assigned_fellow)
                previous_fellow = assigned_fellow

        # Tally days off
        assigned_people = entry["assignments"]
        for person in days_off:
            if person not in assigned_people and weekday >= 5:
                days_off[person] += 1

        schedule.append(entry)
    
    return schedule, days_off

# Prompt for input
start_month = int(input("Enter the starting month (1-12): "))
num_fellows = int(input("Enter the number of fellows: "))
num_residents = int(input("Enter the number of residents: "))

schedule, days_off = generate_schedule(start_month, num_fellows, num_residents)

# Output schedule
for day in schedule:
    print(f"{day['date']}: {', '.join(day['assignments']) if day['assignments'] else 'Off'}")

# Output days off
print("\nDays off for each person:")
for person, off_days in days_off.items():
    print(f"{person}: {off_days} days off")
