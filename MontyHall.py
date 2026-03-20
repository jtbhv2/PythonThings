import random

def playMontyHall():
    possibleDoors = [1,2,3]
    prizeDoor = random.choice(possibleDoors)
    userinput = int(input('Pick door 1, 2, or 3: '))
    while userinput not in possibleDoors:
        userinput = int(input('Invalid input. Please pick door 1, 2, or 3: '))
    hostOptions = [d for d in possibleDoors if d != userinput and d != prizeDoor]
    hostChoice = random.choice(hostOptions)
    print(f"The host opens door {hostChoice} which has a goat behind it.")
    switchOption = [d for d in possibleDoors if d != userinput and d != hostChoice][0]
    switch = input(f"Do you want to switch to door {switchOption}? (y/n): ").lower()
    if switch == 'y':
        userinput = switchOption
    if userinput == prizeDoor:
        print("Congratulations! You won the car!")
    else:
        print("Sorry, you got a goat. Better luck next time!")

def simulateMontyHall(trials):
    switchWins = 0
    stayWins = 0
    for _ in range(trials):
        possibleDoors = [1,2,3]
        prizeDoor = random.choice(possibleDoors)
        userinput = random.choice(possibleDoors)
        hostOptions = [d for d in possibleDoors if d != userinput and d != prizeDoor]
        hostChoice = random.choice(hostOptions)
        switchOption = [d for d in possibleDoors if d != userinput and d != hostChoice][0]
        
        # Simulate switching
        if switchOption == prizeDoor:
            switchWins += 1
        
        # Simulate staying
        if userinput == prizeDoor:
            stayWins += 1
            
    print(f"Switching wins: {switchWins} out of {trials} ({(switchWins/trials)*100:.2f}%)")
    print(f"Staying wins: {stayWins} out of {trials} ({(stayWins/trials)*100:.2f}%)")
    
choice = input("Do you want to play the Monty Hall game or run a simulation? (p/s): ").lower()
if choice == 'p':
    playMontyHall()
elif choice == 's':
    trials = int(input("Enter the number of simulations to run: "))
    simulateMontyHall(trials)
else:    print("Invalid choice. Please enter 'p' or 's'.")