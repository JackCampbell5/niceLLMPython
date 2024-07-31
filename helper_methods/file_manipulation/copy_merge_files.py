import os
import shutil


def copy_and_merge_files(file_list_path, source_dir, dest_dir):
    """
    Copy file names from the file list from the source directory to the destination directory. Also prints teh
    contents of the file to a big file.
    :param file_list_path: The list of files to copy and print
    :param source_dir: Where the file currently is
    :param dest_dir: Where you want the file to go
    :return:
    """
    # Ensure destination directory exists
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    new_file_path = dest_dir + "/aAllFiles1.txt"
    # Open the merged file in write mode
    with open(new_file_path, 'w') as merged_file:
        # Read the list of file names
        with open(file_list_path, 'r') as file_list:
            for file_name in file_list:
                print(f"Processing {file_name}")
                # Remove any surrounding whitespace or newlines
                file_name = file_name.strip()

                # Create full paths
                source_file_path = os.path.join(source_dir, file_name)
                dest_file_path = os.path.join(dest_dir, file_name)

                # Copy the file
                shutil.copy2(source_file_path, dest_file_path)

                # Append the contents of the file to the merged file
                with open(source_file_path, 'r') as source_file:
                    merged_file.write(f"\n{file_name}:\n")
                    merged_file.write(source_file.read())
                    merged_file.write("\n")  # Add a newline to separate file contents


if __name__ == "__main__":
    file_list = os.path.expanduser("~/Documents/niceLLM/output/Correct/hello.txt")  # Where all the files are
    start = os.path.expanduser("~/Documents/niceLLM/output/Correct")  # Where all the files are
    end = os.path.expanduser("~/Documents/niceLLM/output/Correct1")  # Where all the files are

    copy_and_merge_files(file_list, start, end)
