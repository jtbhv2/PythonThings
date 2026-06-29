import random
import time
import os

# ANSI color helpers
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"

def spin_wheel(options):
    random.shuffle(options)

    ticks = random.randint(25, 45)
    delay = 0.03

    for i in range(ticks):
        os.system('cls' if os.name == 'nt' else 'clear')
        index = i % len(options)

        print(f"{BOLD}{CYAN}Spinning...{RESET}\n")

        for j, opt in enumerate(options):
            if j == index:
                arrow = f"{YELLOW}{BOLD}→{RESET}"
                text = f"{GREEN}{BOLD}{opt}{RESET}"
            else:
                arrow = " "
                text = f"{MAGENTA}{opt}{RESET}"

            print(f"{arrow} {text}")

        delay *= 1.10
        time.sleep(delay)

    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{BOLD}{CYAN}Final result:{RESET}\n")

    for j, opt in enumerate(options):
        if j == index:
            arrow = f"{YELLOW}{BOLD}→{RESET}"
            text = f"{GREEN}{BOLD}{opt}{RESET}"
        else:
            arrow = " "
            text = f"{MAGENTA}{opt}{RESET}"

        print(f"{arrow} {text}")

    print(f"\n🎉 {BOLD}Selected:{RESET} {GREEN}{BOLD}{options[index]}{RESET}")


options = ["Harrow the Ninth BSL", "Harrow the Ninth RR", "A Spell for Heartsickness AR", "The Blade Itself MT", "Dungeon Crawler Carl 2 EG", "Harrow the Ninth LN ", "Dungeon Crawler Carl 2 GM"]
spin_wheel(options)
