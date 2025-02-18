import random
import calendar
from collections import defaultdict

def getMonthDays(year, month):
    return calendar.monthrange(year, month)[1]

class Fellow:
    def __init__(self, name):
        self.name = name
        self.shifts = []

class Resident:
    def __init__(self, name):
        self.name = name
        self.shifts = []

def distributeShifts(year, month, fellows, residents):
    numDays = getMonthDays(year, month)
    schedule = defaultdict(lambda: {'fellow': None, 'resident': None, 'traumaBackup': None})
    
    firstWeekday = calendar.monthrange(year, month)[0]  # 0 = Monday, 6 = Sunday
    residentDaysOff = max(1, int(0.15 * numDays))
    residentOffDays = random.sample(range(numDays), residentDaysOff * len(residents))
    residentOffMap = defaultdict(list)
    for i, day in enumerate(residentOffDays):
        residentOffMap[residents[i % len(residents)].name].append(day)
    
    weekendsOff = []
    if len(fellows) >= 2:
        weekends = [(d, (firstWeekday + d - 1) % 7) for d in range(1, numDays + 1) if (firstWeekday + d - 1) % 7 in [4, 5, 6]]
        random.shuffle(weekends)
        weekendsOff = {f.name: [] for f in fellows}
        for fellow in fellows:
            for _ in range(2):
                if weekends:
                    day, _ = weekends.pop()
                    weekendsOff[fellow.name].append(day)
    
    for day in range(numDays):
        weekday = (firstWeekday + day) % 7  # Get actual weekday
        availableFellows = [f for f in fellows if day + 1 not in weekendsOff.get(f.name, [])]
        availableResidents = [r for r in residents if day + 1 not in residentOffMap[r.name]]
        
        if availableFellows and (weekday >= 4 or not availableResidents):
            fellow = random.choice(availableFellows)
            schedule[day + 1]['fellow'] = fellow.name
            fellow.shifts.append(day + 1)
            if weekday in [5, 6]:  # Weekend
                schedule[day + 1]['traumaBackup'] = fellow.name
        
        if availableResidents and (weekday < 4 or not availableFellows):
            resident = random.choice(availableResidents)
            schedule[day + 1]['resident'] = resident.name
            resident.shifts.append(day + 1)
            if weekday == 4 and availableFellows:  # Friday
                schedule[day + 1]['traumaBackup'] = fellow.name if fellow else None
    
    return schedule

def printSchedule(year, month, schedule, fellows, residents):
    print(f"\nSchedule for {calendar.month_name[month]} {year}")
    for day in range(1, getMonthDays(year, month) + 1):
        weekdayName = calendar.day_name[calendar.weekday(year, month, day)]
        fellow = schedule[day]['fellow'] if schedule[day]['fellow'] else "None"
        resident = schedule[day]['resident'] if schedule[day]['resident'] else "None"
        traumaBackup = schedule[day]['traumaBackup'] if schedule[day]['traumaBackup'] else "None"
        print(f"{day:2} {weekdayName}: Fellow: {fellow}, Resident: {resident}, Trauma Backup: {traumaBackup}")
    
    print("\nDays Off Summary:")
    for fellow in fellows:
        daysOff = getMonthDays(year, month) - len(fellow.shifts)
        print(f"{fellow.name}: {daysOff} days off")
    for resident in residents:
        daysOff = getMonthDays(year, month) - len(resident.shifts)
        print(f"{resident.name}: {daysOff} days off")

def main():
    year = 2025
    startMonth = int(input("Enter starting month number (1-12) for the year 2025: "))
    numMonths = int(input("Enter number of months to generate: "))
    numFellows = int(input("Enter number of fellows: "))
    numResidents = int(input("Enter number of residents: "))
    
    fellows = [Fellow(f'Fellow{i+1}') for i in range(numFellows)]
    residents = [Resident(f'Resident{i+1}') for i in range(numResidents)]
    
    for month in range(startMonth, min(startMonth + numMonths, 13)):
        schedule = distributeShifts(year, month, fellows, residents)
        printSchedule(year, month, schedule, fellows, residents)

if __name__ == "__main__":
    main()
