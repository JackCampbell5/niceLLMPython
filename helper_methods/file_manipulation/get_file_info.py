import os
import time


def find_earliest_modified_date(directory):
    """
    Goes through the given directory including all its sub folders, and find the earliest file modified date and
    time
    :param directory: The directory to search through
    :return: The date, the file name
    """
    earliest_date = None
    earliest_file = None

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_modified_date = os.path.getmtime(file_path)
            if earliest_date is None or file_modified_date < earliest_date:
                earliest_date = file_modified_date
                earliest_file = file_path

    if earliest_date is not None:
        return time.strftime('%m/%d/%Y', time.gmtime(earliest_date)), earliest_file
    else:
        return None, None


def get_num_experiments(file_path):
    """
    Gets and returns a dictionary of counts for each experiment number in the directory.
    :param file_path: The directory to search through
    :return: A dictionary with experimentNum:"count found
    """
    retDic = {}
    for line in os.listdir(file_path):
        exp = line[line.find("(") + 1:line.find(")")]
        if exp in retDic:
            retDic[exp] += 1
        else:
            retDic[exp] = 1
    return len(retDic)


def find_file_with_most_lines(directory):
    """
    Finds the file with the most lines in the given directory
    :param directory: The directory to search through
    :return: The file name and how many lines it has
    """
    max_lines = 0
    file_with_most_lines = None
    parent_dir = os.path.join(os.path.dirname(directory), "MoreCorrect")

    # Loop through the directory
    with open(directory, 'r') as file_names:
        for file_name in file_names.readlines():
            file_name = file_name.strip()
            print(file_name)
            file_path = os.path.join(parent_dir, file_name)

            # Check if it is a file
            if os.path.isfile(file_path):
                try:
                    with open(file_path, 'r') as file:
                        # Count the number of lines in the file
                        num_lines = sum(1 for line in file)

                        # Update the file with the most lines
                        if num_lines > max_lines:
                            max_lines = num_lines
                            file_with_most_lines = file_name
                except Exception as e:
                    print(f"Could not read file {file_name}: {e}")

    return file_with_most_lines, max_lines


def find_files_with_least_lines(directory):
    """
    Finds the top 10 files with the least lines and returns an array of them
    :param directory: The directory to search through
    :return: An array with the top 10 files
    """
    file_line_counts = []
    ret_dict = []

    parent_dir = os.path.join(os.path.dirname(directory), "MoreCorrect")

    # Loop through the directory
    with open(directory, 'r') as file_names:
        for file_name in file_names.readlines():
            file_name = file_name.strip()
            # print(file_name)
            file_path = os.path.join(parent_dir, file_name)
            # Check if it is a file
            if os.path.isfile(file_path):
                try:
                    with open(file_path, 'r') as file:
                        # Count the number of lines in the file
                        num_lines = sum(1 for line in file)
                        # Append the file and its line count to the list
                        ret_dict.append(num_lines)
                        # file_line_counts.append((file_name, num_lines))
                except Exception as e:
                    print(f"Could not read file {file_name}: {e}")

    # Sort the list by the number of lines
    file_line_counts.sort(key=lambda x: x[1])

    # Get the top 10 files with the smallest number of lines
    top_10_files = file_line_counts[:10]

    return top_10_files


if __name__ == "__main__":
    directory = os.path.expanduser("~/Documents/niceLLM/output/LiveFiles")
    print(find_earliest_modified_date(directory))
    print(get_num_experiments(directory))
    print(find_file_with_most_lines(directory))
    print(find_files_with_least_lines(directory))
