import tkinter as tk
from tkinter import messagebox
import kociemba

def validateCubeInput(cubeInput):
    colorCounts = {}
    for color in cubeInput.values():
        colorCounts[color] = colorCounts.get(color, 0) + 1
    
    if any(count != 9 for count in colorCounts.values()):
        return False, "Each color must appear exactly 9 times."
    return True, "Valid input."

def getCubeString():
    cubeInput = {pos: entries[pos].get() for pos in positions}
    isValid, message = validateCubeInput(cubeInput)
    
    if not isValid:
        messagebox.showerror("Error", message)
        return
    
    cubeString = ''.join(cubeInput[pos] for pos in positions)
    try:
        solution = kociemba.solve(cubeString)
        optimizedSolution = solution  # Placeholder for further optimizations
        resultLabel.config(text=f"Solution: {solution}\nOptimized: {optimizedSolution}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title("Rubik's Cube Solver")

entries = {}
positions = [
    "U1", "U2", "U3", "U4", "U5", "U6", "U7", "U8", "U9",
    "L1", "L2", "L3", "L4", "L5", "L6", "L7", "L8", "L9",
    "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9",
    "R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9",
    "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9",
    "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9",
]

frame = tk.Frame(root)
frame.pack()

for i, pos in enumerate(positions):
    tk.Label(frame, text=pos).grid(row=i // 9, column=(i % 9) * 2)
    entry = tk.Entry(frame, width=3)
    entry.grid(row=i // 9, column=(i % 9) * 2 + 1)
    entries[pos] = entry

tk.Button(root, text="Solve", command=getCubeString).pack()
resultLabel = tk.Label(root, text="")
resultLabel.pack()

root.mainloop()
