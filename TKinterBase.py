import tkinter as tk  # Import the tkinter library for GUI applications
from tkinter import filedialog  # Import file dialog module for opening files and folders

# Create the main application window
root = tk.Tk()  # Initialize the Tkinter root window
root.title("Learning Tkinter GUI")  # Set the title of the window
root.geometry("500x400")  # Set the initial size of the window

# Function to open a file dialog and update the entry box
def browseFiles():
    filename = filedialog.askopenfilename(title="Select a File")  # Open file dialog to pick a file
    fileEntry.delete(0, tk.END)  # Clear any existing text in the entry box
    fileEntry.insert(0, filename)  # Insert the selected file path into the entry box

# Function to open a folder dialog and update the entry box
def browseFolders():
    foldername = filedialog.askdirectory(title="Select a Folder")  # Open folder dialog to pick a directory
    fileEntry.delete(0, tk.END)  # Clear any existing text in the entry box
    fileEntry.insert(0, foldername)  # Insert the selected folder path into the entry box

# Function to clear the output box and print a message
def button1Function():
    outputBox.delete(1.0, tk.END)  # Clear the output box
    outputBox.insert(tk.END, "Hello, World!\n")  # Insert new text

# Dummy functions for other buttons and checkboxes
def button2Function():
    pass  # Replace 'pass' with actual logic

def button3Function():
    pass  # Replace 'pass' with actual logic

def checkbox1Function():
    pass  # Replace 'pass' with actual logic

def checkbox2Function():
    pass  # Replace 'pass' with actual logic

def checkbox3Function():
    pass  # Replace 'pass' with actual logic

# Label and Text Entry for user input
tk.Label(root, text="Enter Text:").pack(pady=5)  # Create a label for the text entry box
textEntry = tk.Entry(root, width=50)  # Create a text entry box where users can type
textEntry.pack(pady=5)  # Pack it onto the window with spacing

# Label and File/Folder Selection Widgets
tk.Label(root, text="Select a File or Folder:").pack(pady=5)  # Label for file/folder selection
fileFrame = tk.Frame(root)  # Create a frame to group file entry and browse button
fileFrame.pack(pady=5)  # Pack the frame onto the window with spacing

fileEntry = tk.Entry(fileFrame, width=40)  # Entry box for file/folder path
fileEntry.pack(side=tk.LEFT, padx=5)  # Pack entry box to the left with padding

browseButton = tk.Button(fileFrame, text="Browse", command=browseFiles)  # Button to open file dialog
browseButton.pack(side=tk.LEFT)  # Pack the button next to the entry box

# Buttons assigned to functions
tk.Button(root, text="Button 1", command=button1Function).pack(pady=5)  # Creates a button and assigns function
tk.Button(root, text="Button 2", command=button2Function).pack(pady=5)  # Another button with function
tk.Button(root, text="Button 3", command=button3Function).pack(pady=5)  # Another button with function

# Checkboxes assigned to dummy functions
checkVar1 = tk.BooleanVar()  # Variable to store checkbox state (True/False)
checkVar2 = tk.BooleanVar()
checkVar3 = tk.BooleanVar()

tk.Checkbutton(root, text="Checkbox 1", variable=checkVar1, command=checkbox1Function).pack()  # Create a checkbox
tk.Checkbutton(root, text="Checkbox 2", variable=checkVar2, command=checkbox2Function).pack()  # Another checkbox
tk.Checkbutton(root, text="Checkbox 3", variable=checkVar3, command=checkbox3Function).pack()  # Another checkbox

# Output Box (Text Widget) to display information or messages
tk.Label(root, text="Output:").pack(pady=5)  # Label for output box
outputBox = tk.Text(root, height=5, width=50)  # Create a multi-line text box for output
outputBox.pack(pady=5)  # Pack the output box onto the window with spacing

# Run the Tkinter main loop to display the GUI
root.mainloop()  # Keeps the window open and listens for user actions
