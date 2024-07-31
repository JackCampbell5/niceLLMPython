import os
"""Checks if the text in the file is present in any files in the given directory"""


def get_documents_folder():
    home = os.path.expanduser("~")
    documents_folder = os.path.join(home, 'Documents')
    return documents_folder


def read_search_text_from_file(directory, filename):
    file_path = os.path.join(directory, filename)
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read().strip()  # Remove any surrounding whitespace
    except Exception as e:
        print(f"Could not read the search text file: {file_path}. Error: {e}")
        return None


def search_text_in_files(directory, search_text):
    num = 0
    if search_text is None:
        return
    # Loop through all files in the directory
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                # Open and read each file
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    # Check if the search text is in the file content
                    if search_text in content:
                        print(f"Text found in: {file_path}")
                        num+=1
            except Exception as e:
                print(f"Could not read file: {file_path}. Error: {e}")
    return num

subfolder = "24-6-11b"
# Example usage
documents_folder = os.path.expanduser("~/Documents/extracted_files")

extracted_files_folder = os.path.join(documents_folder, subfolder)
search_text_file = 'search_text.txt'  # Replace with the name of the file containing the search text

search_text = read_search_text_from_file(documents_folder, search_text_file)
num_found = search_text_in_files(extracted_files_folder, search_text)
print(f"That text was found {num_found} times in {search_text_file}")



