import os
from datetime import datetime

def rename_images(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        if os.path.isfile(file_path) and filename.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp")):
            modification_time = os.path.getmtime(file_path) #%S%f
            timestamp = datetime.fromtimestamp(modification_time).strftime("%Y%m%d_%H%M%S")

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
directory_path = r"./"  # Replace with your directory path
rename_images(directory_path)
