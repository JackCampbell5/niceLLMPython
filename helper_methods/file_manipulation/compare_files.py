import os

"""
Takes 2 files containing list of files and compare there contents to see how many different names they have.
"""


def compare_files(path1, path2):
    with open(path1, 'r') as file:
        files1 = set(line.strip() for line in file)

    with open(path2, 'r') as file:
        files2 = set(line.strip() for line in file)

    in_file1_not_in_file2 = files1 - files2
    in_file2_not_in_file1 = files2 - files1

    print(f"Files in {file1} but not in {file2}:")
    for file_name in in_file1_not_in_file2:
        print(file_name)

    print(f"\nFiles in {file2} but not in {file1}:")
    for file_name in in_file2_not_in_file1:
        print(file_name)


if __name__ == "__main__":
    filenames_path = os.path.expanduser("~/Documents/niceLLM/output/")
    file1 = '24-7-3ediWrong.txt'
    file2 = '24-7-3SimList0.5.txt'
    compare_files(os.path.join(filenames_path, file1), os.path.join(filenames_path, file2))
