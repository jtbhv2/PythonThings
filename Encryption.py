import os
import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.fernet import Fernet
import shutil

# Function to generate a new key
def generate_key():
    return Fernet.generate_key()

# Function to save the key to a file
def save_key_to_file(key, file_path):
    key_file_path = file_path + '.key'  # Save key with a .key extension
    with open(key_file_path, 'wb') as key_file:
        key_file.write(key)
    return key_file_path

# Function to load the key from a file
def load_key_from_file():
    key_file = filedialog.askopenfilename(filetypes=[("Key Files", "*.key")])
    if key_file:
        try:
            with open(key_file, 'rb') as file:
                key = file.read()
            return key
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load key: {e}")
            return None
    return None

# Function to encrypt or decrypt a file
def process_file(file_path, key, encrypt=True):
    cipher_suite = Fernet(key)
    
    try:
        with open(file_path, 'rb') as file:
            file_data = file.read()

        if encrypt:
            encrypted_data = cipher_suite.encrypt(file_data)
        else:
            encrypted_data = cipher_suite.decrypt(file_data)

        output_file = file_path + '.enc' if encrypt else file_path[:-4]
        with open(output_file, 'wb') as file:
            file.write(encrypted_data)
        
        return output_file
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return None

# Function to recursively process all files in a folder
def process_folder(folder_path, key, encrypt=True):
    output_folder = folder_path + '_enc' if encrypt else folder_path + '_dec'
    os.makedirs(output_folder, exist_ok=True)

    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            relative_path = os.path.relpath(file_path, folder_path)
            output_file_path = os.path.join(output_folder, relative_path)

            os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
            result = process_file(file_path, key, encrypt)

            if result:
                shutil.move(result, output_file_path)
            else:
                messagebox.showerror("Error", f"Failed to process file: {file_path}")
                return False
    return True

# GUI function for user interaction
def start_gui():
    def on_encrypt():
        key_input = key_entry.get()
        if key_input == "":
            messagebox.showerror("Error", "Key cannot be empty.")
            return

        try:
            key = bytes(key_input, 'utf-8')
            cipher_suite = Fernet(key)
        except:
            messagebox.showerror("Error", "Invalid key format.")
            return

        file_or_folder = file_input.get()
        output_location = output_input.get()

        if os.path.isdir(file_or_folder):
            if process_folder(file_or_folder, key, encrypt=True):
                messagebox.showinfo("Success", f"Folder encrypted successfully!")
        elif os.path.isfile(file_or_folder):
            output_file = process_file(file_or_folder, key, encrypt=True)
            if output_file:
                messagebox.showinfo("Success", f"File encrypted successfully! Output: {output_file}")
        else:
            messagebox.showerror("Error", "Selected path is not valid.")

    def on_decrypt():
        key_input = key_entry.get()
        if key_input == "":
            messagebox.showerror("Error", "Key cannot be empty.")
            return

        try:
            key = bytes(key_input, 'utf-8')
            cipher_suite = Fernet(key)
        except:
            messagebox.showerror("Error", "Invalid key format.")
            return

        file_or_folder = file_input.get()
        output_location = output_input.get()

        if os.path.isdir(file_or_folder):
            if process_folder(file_or_folder, key, encrypt=False):
                messagebox.showinfo("Success", f"Folder decrypted successfully!")
        elif os.path.isfile(file_or_folder):
            output_file = process_file(file_or_folder, key, encrypt=False)
            if output_file:
                messagebox.showinfo("Success", f"File decrypted successfully! Output: {output_file}")
        else:
            messagebox.showerror("Error", "Selected path is not valid.")

    def browse_file():
        filename = filedialog.askopenfilename()
        if filename:
            file_input.delete(0, tk.END)
            file_input.insert(0, filename)

    def browse_folder():
        foldername = filedialog.askdirectory()
        if foldername:
            file_input.delete(0, tk.END)
            file_input.insert(0, foldername)

    def generate_new_key():
        new_key = generate_key()
        key_entry.delete(0, tk.END)
        key_entry.insert(0, new_key.decode())

        # If the key is generated, save it to a file
        file_or_folder = file_input.get()
        key_file_path = save_key_to_file(new_key, file_or_folder)

        messagebox.showinfo("Key Saved", f"New key saved to: {key_file_path}")

    def load_key():
        key = load_key_from_file()
        if key:
            key_entry.delete(0, tk.END)
            key_entry.insert(0, key.decode())

    window = tk.Tk()
    window.title("File/Folders Encryptor/Decryptor")

    # Input for file/folder
    file_input_label = tk.Label(window, text="Select File or Folder:")
    file_input_label.grid(row=0, column=0, padx=10, pady=10)
    file_input = tk.Entry(window, width=40)
    file_input.grid(row=0, column=1, padx=10, pady=10)
    browse_file_button = tk.Button(window, text="Browse File", command=browse_file)
    browse_file_button.grid(row=0, column=2, padx=10, pady=10)
    browse_folder_button = tk.Button(window, text="Browse Folder", command=browse_folder)
    browse_folder_button.grid(row=0, column=3, padx=10, pady=10)

    # Key input
    key_input_label = tk.Label(window, text="Enter or Generate Key:")
    key_input_label.grid(row=1, column=0, padx=10, pady=10)
    key_entry = tk.Entry(window, width=40)
    key_entry.grid(row=1, column=1, padx=10, pady=10)
    generate_key_button = tk.Button(window, text="Generate New Key", command=generate_new_key)
    generate_key_button.grid(row=1, column=2, padx=10, pady=10)

    # Load key from file
    load_key_button = tk.Button(window, text="Load Key from File", command=load_key)
    load_key_button.grid(row=1, column=3, padx=10, pady=10)

    # Output location input
    output_input_label = tk.Label(window, text="Output Location (Optional):")
    output_input_label.grid(row=2, column=0, padx=10, pady=10)
    output_input = tk.Entry(window, width=40)
    output_input.grid(row=2, column=1, padx=10, pady=10)
    
    # Encrypt/Decrypt buttons
    encrypt_button = tk.Button(window, text="Encrypt", command=on_encrypt)
    encrypt_button.grid(row=3, column=1, padx=10, pady=10)

    decrypt_button = tk.Button(window, text="Decrypt", command=on_decrypt)
    decrypt_button.grid(row=3, column=2, padx=10, pady=10)

    window.mainloop()

# Start the GUI
if __name__ == "__main__":
    start_gui()
