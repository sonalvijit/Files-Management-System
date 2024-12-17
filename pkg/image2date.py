import os
from datetime import datetime

def rename_images(directory):
    # Iterate over files in the directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        # Process only files that are images (common formats)
        if os.path.isfile(file_path) and filename.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp")):
            # Get the modification time of the file
            modification_time = os.path.getmtime(file_path)
            timestamp = datetime.fromtimestamp(modification_time).strftime("%Y%m%d_%H%M%S%f")

            # Create the new filename
            file_extension = os.path.splitext(filename)[1]
            renamed_filename = f"{timestamp}{file_extension}"
            renamed_file_path = os.path.join(directory, renamed_filename)

            # Ensure unique filenames
            counter = 1
            while os.path.exists(renamed_file_path):
                renamed_filename = f"{timestamp}_{counter}{file_extension}"
                renamed_file_path = os.path.join(directory, renamed_filename)
                counter += 1

            # Rename the original file
            os.rename(file_path, renamed_file_path)

# Specify the directory containing the images
# directory_path = r"E:\T2024\12-2015"  # Replace with your directory path
# rename_images(directory_path)
