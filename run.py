import os
import shutil
from datetime import datetime
from collections import defaultdict
from tqdm import tqdm

def classify_files_in_folder(folder_path, include_subfolders=False):
    """
    Scans the specified folder and optionally its subfolders, classifying files based on their extensions.

    Args:
        folder_path (str): The path of the folder to scan.
        include_subfolders (bool): Whether to include files in subfolders.

    Returns:
        dict: A dictionary with file extensions as keys and their counts as values.
    """
    # Dictionary to hold counts of each file type
    file_counts = defaultdict(int)

    try:
        if include_subfolders:
            # Walk through the directory and its subdirectories
            for root, _, files in os.walk(folder_path):
                for file in files:
                    _, extension = os.path.splitext(file)
                    extension = extension.lower()
                    file_counts[extension] += 1
        else:
            # List all items in the folder
            for item in os.listdir(folder_path):
                item_path = os.path.join(folder_path, item)
                
                # Process only files, skip directories
                if os.path.isfile(item_path):
                    # Extract the file extension (e.g., '.txt')
                    _, extension = os.path.splitext(item)
                    # Normalize the extension to lowercase (e.g., '.TXT' -> '.txt')
                    extension = extension.lower()
                    # Increment the count for this file type
                    file_counts[extension] += 1

    except Exception as e:
        print(f"Error scanning folder: {e}")

    return dict(file_counts)

def copy_files_to_folders(folder_path, destination_base):
    """
    Copies files starting with specific prefixes to folders named by their creation date (MM-YYYY).
    Files not matching the prefixes are copied to an 'unknown' folder.

    Args:
        folder_path (str): The path of the folder to scan.
        destination_base (str): The base path where categorized folders will be created.
    """
    prefixes = ("2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024", "DecoPic", "DOC", "IMG")

    try:
        files = [item for item in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, item))]

        with tqdm(total=len(files), desc="Copying Files", unit="file") as progress_bar:
            for item in files:
                item_path = os.path.join(folder_path, item)

                if item.startswith(prefixes):
                    # Get file creation time
                    creation_time = datetime.fromtimestamp(os.path.getctime(item_path))
                    folder_name = creation_time.strftime("%m-%Y")
                else:
                    # Files without matching prefixes go to 'unknown' folder
                    folder_name = "unknown"

                destination_folder = os.path.join(destination_base, folder_name)

                # Create the destination folder if it doesn't exist
                os.makedirs(destination_folder, exist_ok=True)

                # Copy the file to the destination folder
                shutil.copy2(item_path, os.path.join(destination_folder, item))

                progress_bar.update(1)

    except Exception as e:
        print(f"Error copying files: {e}")

if __name__ == "__main__":
    folder_path = input("Enter the folder path to scan: ").strip()
    include_subfolders = input("Include subfolders? (yes/no): ").strip().lower() == "yes"
    destination_base = input("Enter the destination base folder for copying files: ").strip()
    
    if os.path.isdir(folder_path) and os.path.isdir(destination_base):
        result = classify_files_in_folder(folder_path, include_subfolders=include_subfolders)
        print("\nFile type counts in the folder:")
        for ext, count in sorted(result.items()):
            print(f"{ext if ext else 'No Extension'}: {count}")

        copy_files_to_folders(folder_path, destination_base)
        print("\nFiles have been copied to their respective folders.")
    else:
        print("The specified paths are not valid folders.")
