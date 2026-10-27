import os
import shutil
import tkinter as tk
from tkinter import filedialog

# Extension mapping dictionary
mapping = {
    '.pdf': 'Documents', 
    '.mkv': 'Videos',
    '.mp3': 'Videos',
    '.jpg': 'Images', 
    '.png': 'Images', 
    '.zip': 'Archives'
}

# Open a file explorer popup to select the folder
root = tk.Tk()
root.withdraw() # Hide the main tkinter window
target_dir = filedialog.askdirectory(title="Select Folder to Sort")

moved_files = []

if target_dir:
    with os.scandir(target_dir) as entries:
        for entry in entries:
            if entry.is_file():
                ext = os.path.splitext(entry.name)[1].lower()
                folder_name = mapping.get(ext, 'Unsupported')
                
                dest_folder = os.path.join(target_dir, folder_name)
                os.makedirs(dest_folder, exist_ok=True)
                
                try:
                    shutil.move(entry.path, os.path.join(dest_folder, entry.name))
                    moved_files.append(entry.name)
                except (FileExistsError, PermissionError):
                    pass

    # Save log in the script's directory
    log_path = os.path.join(os.path.dirname(__file__), "moved_files_log.txt")
    with open(log_path, "w") as log:
        log.write("\n".join(moved_files))

    print(f"\nExecution Summary: Total files relocated = {len(moved_files)}")
else:
    print("No folder selected.")