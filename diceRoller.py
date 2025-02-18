import tkinter as tk
import random

class DiceRollerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dice Roller")
        
        self.dice_options = [2, 4, 6, 8, 10, 12, 20, 100]
        self.selected_dice = {}
        self.roll_selections = {}

        # Adding dice options as buttons
        self.dice_buttons = {}
        for i, sides in enumerate(self.dice_options):
            button = tk.Button(root, text=str(sides), width=5, command=lambda sides=sides: self.toggle_die(sides))
            button.grid(row=i, column=0, padx=5, pady=5)
            self.dice_buttons[sides] = button

            roll_frame = tk.Frame(root)
            roll_frame.grid(row=i, column=1, padx=5)
            self.roll_selections[sides] = tk.IntVar(value=1)

            for j in range(1, 6):
                roll_button = tk.Radiobutton(roll_frame, text=str(j), variable=self.roll_selections[sides], value=j)
                roll_button.pack(side=tk.LEFT)

        # Roll button
        self.roll_button = tk.Button(root, text="Roll Dice", command=self.roll_dice)
        self.roll_button.grid(row=len(self.dice_options), column=0, columnspan=2, pady=10)

        # Results label
        self.result_label = tk.Label(root, text="Roll results will appear here.")
        self.result_label.grid(row=len(self.dice_options)+1, column=0, columnspan=2)

    def toggle_die(self, sides):
        if sides in self.selected_dice:
            del self.selected_dice[sides]
            self.dice_buttons[sides].config(relief="raised")
        else:
            self.selected_dice[sides] = True
            self.dice_buttons[sides].config(relief="sunken")

    def roll_dice(self):
        roll_results = []
        total_sum = 0
        total_count = 0

        for sides in self.selected_dice:
            rolls = self.roll_selections[sides].get()
            rolls_list = [random.randint(1, sides) for _ in range(rolls)]
            roll_sum = sum(rolls_list)
            roll_results.append((sides, rolls, rolls_list, roll_sum, roll_sum / rolls))
            total_sum += roll_sum
            total_count += rolls

        result_text = ""
        for sides, rolls, rolls_list, roll_sum, roll_avg in roll_results:
            result_text += f"{sides}-sided die:\nRolls: {rolls_list}\nSum: {roll_sum}\nAverage: {roll_avg:.2f}\n\n"

        if total_count > 0:
            total_avg = total_sum / total_count
            result_text += f"Total Sum for All: {total_sum}\nTotal Average for All: {total_avg:.2f}\n"

        self.result_label.config(text=result_text)

# Tkinter setup
root = tk.Tk()
app = DiceRollerApp(root)
root.mainloop()
