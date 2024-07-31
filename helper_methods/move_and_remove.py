import os
import shutil


def move_files_and_remove_dirs(source_dir, destination_dir):
    """
    Moves all files from the source directory to the destination directory and removes
    all directories in the source directory
    :param source_dir: Path to the source directory
    :param destination_dir: Path to the destination directory
    :return: None
    """
    # Ensure the destination directory exists
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    # Walk through the source directory
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            # Construct full file path
            file_path = os.path.join(root, file)
            # Move file to destination directory
            shutil.move(file_path, destination_dir)
        for dir in dirs:
            # Construct full directory path
            dir_path = os.path.join(root, dir)
            # Remove directory
            shutil.rmtree(dir_path)


if __name__ == "__main__":
    start = os.path.expanduser("~/Documents/niceLLM/output/Correct")  # Where all the files are
    end = os.path.expanduser("~/Documents/niceLLM/output/Correct1")  # Where all the files are
    move_files_and_remove_dirs(start, end)
