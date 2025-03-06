#Deletes all files in the specified folder. 
#Sends to recycle bin

import os
import send2trash

def movetoRB(folderPath):
    if not os.path.exists(folderPath):
        print("Folder not found!")
        return
    
    for file in os.listdir(folderPath):
        filePath = os.path.join(folderPath, file)
        if os.path.isfile(filePath):
            send2trash.send2trash(filePath)
            print(f"Moved to Recycle Bin: {filePath}")

movetoRB(r"C:\Users\Public\Desktop")
