"""
Move files with file names in the file list from the starting to ending folder
"""
import os
import shutil

from helper_methods.extract_helpers import print_error


def move_list(file_list_path, starting_folder, destination_folder):
    # Ensure the destination folder exists
    os.makedirs(destination_folder, exist_ok=True)

    # Read the list of file paths
    with open(file_list_path, 'r') as file:
        file_paths = file.readlines()

    # Move each file to the destination folder
    for file_path in file_paths:
        file_path = file_path.strip()  # Remove any leading/trailing whitespace
        new_path = os.path.join(starting_folder, file_path)
        if os.path.isfile(new_path):
            shutil.move(new_path, destination_folder)
            print(f"Moved: {new_path}")
        else:
            print_error(f"File not found: {new_path}")


if __name__ == "__main__":
    file_list = os.path.expanduser("~/Documents/niceLLM/DebugFiles/24-7-3 Files With the Editor Tag.txt")

    starting = os.path.expanduser("~/Documents/niceLLM/output/Correct(Errors)")
    ending = os.path.expanduser("~/Documents/niceLLM/output/desErrors")

    move_list(file_list, starting, ending)
