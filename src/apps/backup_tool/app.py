import os
import shutil
import datetime
import logging
import tkinter as tk
from tkinter.filedialog import askdirectory

def main():
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Hide the main tkinter window
    root = tk.Tk()
    root.withdraw()
    
    print("Please select the folder you want to backup...")
    select_folder = askdirectory(title="Select Folder to Backup")
    
    if not select_folder:
        logging.warning("No folder selected. Backup cancelled.")
        return

    select_folder = os.path.normpath(select_folder)
    backup_root_name = "backup"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # Destination: source/backup/timestamp/
    backup_dest_dir = os.path.join(select_folder, backup_root_name, timestamp)

    logging.info(f"Starting backup for: {select_folder}")
    logging.info(f"Destination: {backup_dest_dir}")

    # Create destination directory
    try:
        os.makedirs(backup_dest_dir, exist_ok=True)
    except OSError as e:
        logging.error(f"Error creating backup directory '{backup_dest_dir}': {e}")
        return

    items = os.listdir(select_folder)
    count = 0
    
    for item in items:
        # Skip the backup folder itself to avoid infinite recursion if run multiple times
        if item == backup_root_name:
            continue
            
        source_path = os.path.join(select_folder, item)
        dest_path = os.path.join(backup_dest_dir, item)
        
        try:
            if os.path.isfile(source_path):
                shutil.copy2(source_path, dest_path)
                count += 1
            elif os.path.isdir(source_path):
                shutil.copytree(source_path, dest_path)
                count += 1
        except Exception as e:
            logging.error(f"Failed to copy '{item}': {e}")

    logging.info(f"Backup completed! {count} items copied.")
    input("Press Enter to exit...") # Pause to let user see result if launched from cli

if __name__ == "__main__":
    main()