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
    file_counts = defaultdict(int)

    def recursive_scan(path):
        try:
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                if os.path.isfile(item_path):
                    _, extension = os.path.splitext(item)
                    extension = extension.lower()
                    file_counts[extension] += 1
                elif os.path.isdir(item_path):
                    recursive_scan(item_path)
        except Exception as e:
            print(f"Error scanning folder {path}: {e}")

    try:
        if include_subfolders:
            recursive_scan(folder_path)
        else:
            for item in os.listdir(folder_path):
                item_path = os.path.join(folder_path, item)
                if os.path.isfile(item_path):
                    _, extension = os.path.splitext(item)
                    extension = extension.lower()
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
    
    # Helper function to count all files for progress bar initialization
    def count_files(path):
        total_files = 0
        for root, _, files in os.walk(path):
            total_files += len(files)
        return total_files

    # Recursive file copy function with progress bar updates
    def recursive_copy(path, progress_bar):
        try:
            files = [item for item in os.listdir(path) if os.path.isfile(os.path.join(path, item))]
            for item in files:
                item_path = os.path.join(path, item)
                if item.startswith(prefixes):
                    creation_time = datetime.fromtimestamp(os.path.getctime(item_path))
                    folder_name = creation_time.strftime("%m-%Y")
                else:
                    folder_name = "unknown"
                destination_folder = os.path.join(destination_base, folder_name)
                os.makedirs(destination_folder, exist_ok=True)
                shutil.copy2(item_path, os.path.join(destination_folder, item))
                progress_bar.update(1)  # Update the progress bar after copying a file

            subfolders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
            for subfolder in subfolders:
                recursive_copy(os.path.join(path, subfolder), progress_bar)

        except Exception as e:
            print(f"Error copying files from {path}: {e}")

    try:
        if os.path.isdir(folder_path):
            total_files = count_files(folder_path)
            with tqdm(total=total_files, desc="Copying Files", unit="file") as progress_bar:
                recursive_copy(folder_path, progress_bar)
    except Exception as e:
        print(f"Error during file copy: {e}")

# def copy_files_to_folders(folder_path, destination_base):
#     """
#     Copies files starting with specific prefixes to folders named by their creation date (MM-YYYY).
#     Files not matching the prefixes are copied to an 'unknown' folder.

#     Args:
#         folder_path (str): The path of the folder to scan.
#         destination_base (str): The base path where categorized folders will be created.
#     """
#     prefixes = ("2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024", "DecoPic", "DOC", "IMG")

#     def recursive_copy(path):
#         try:
#             files = [item for item in os.listdir(path) if os.path.isfile(os.path.join(path, item))]
#             for item in files:
#                 item_path = os.path.join(path, item)
#                 if item.startswith(prefixes):
#                     creation_time = datetime.fromtimestamp(os.path.getctime(item_path))
#                     folder_name = creation_time.strftime("%m-%Y")
#                 else:
#                     folder_name = "unknown"
#                 destination_folder = os.path.join(destination_base, folder_name)
#                 os.makedirs(destination_folder, exist_ok=True)
#                 shutil.copy2(item_path, os.path.join(destination_folder, item))

#             subfolders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
#             for subfolder in subfolders:
#                 recursive_copy(os.path.join(path, subfolder))

#         except Exception as e:
#             print(f"Error copying files from {path}: {e}")

#     try:
#         if os.path.isdir(folder_path):
#             with tqdm(desc="Copying Files", unit="file") as progress_bar:
#                 recursive_copy(folder_path)
#     except Exception as e:
#         print(f"Error during file copy: {e}")

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
