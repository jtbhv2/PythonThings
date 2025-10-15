import os
import shutil
#this will take all the files in subfolders and move them to the main folder, renaming them to avoid overwrites
input_folder = input("Enter the path to the folder containing subfolders: ")

def flatten_folders(root_folder):
    counter = 1  # Start numbering from 1

    # Loop through all items in the root folder
    for item in os.listdir(root_folder):
        item_path = os.path.join(root_folder, item)

        # If it's a folder, move its contents up
        if os.path.isdir(item_path):
            for sub_item in os.listdir(item_path):
                sub_item_path = os.path.join(item_path, sub_item)
                base, ext = os.path.splitext(sub_item)
                new_name = f"{base}_{counter}{ext}"
                target_path = os.path.join(root_folder, new_name)

                # Ensure unique name even if counter collides
                while os.path.exists(target_path):
                    counter += 1
                    new_name = f"{base}_{counter}{ext}"
                    target_path = os.path.join(root_folder, new_name)

                shutil.move(sub_item_path, target_path)
                counter += 1  # Increment for next file

            # Optionally remove the now-empty folder
            os.rmdir(item_path)

# Example usage

flatten_folders(input_folder)