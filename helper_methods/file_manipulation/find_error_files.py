import os

from helper_methods.extract_helpers import print_to_file


def check_specific_text_in_files(directory, specific_text, save_file_name):
    """
    Looks through every file in the directory for every element in specific_text. Returns a count of the files with
    and without this text. Also creates a file containing all the file names that were not valid

    :param str directory: The directory to search in
    :param str[] specific_text: An array of the text to search for
    :param save_file_name: Name of the output file to create
    :return: An int of those contained as well as not contained
    """
    contains_text_files = 0
    does_not_contain_text_files = 0
    result_arr = []
    contain_inst = {}
    not_contain_inst = {}

    def add_to_dict(file_name, inst_dict):
        inst = file_name[:file_name.find("(")]
        if inst in inst_dict:
            inst_dict[inst] += 1
        else:
            inst_dict[inst] = 1

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            try:
                with open(filepath, 'r', errors='ignore') as file:
                    content = file.read()
                    total = 0
                    for text in specific_text:
                        if text in content:
                            total += 1
                    if total >= 1:
                        add_to_dict(file_name=filename, inst_dict=contain_inst)
                        contains_text_files += 1
                    else:
                        result_arr.append(filename)
                        add_to_dict(file_name=filename, inst_dict=not_contain_inst)
                        does_not_contain_text_files += 1
            except:
                does_not_contain_text_files += 1
    print("Contain", contain_inst)
    result_arr.append(contain_inst)
    print("Not", not_contain_inst)
    result_arr.append(not_contain_inst)
    print_to_file(os.path.dirname(directory), save_file_name, result_arr, "arr")
    return contains_text_files, does_not_contain_text_files


def print_error_file_names():
    """
    Checks how many files have the description tag, the editor tag, or both. Prints all results to a file.
    :return:
    """
    directory = os.path.expanduser("~/Documents/niceLLM/output/Correct")  # Where all the files are

    # Files using the description tag
    print("Description:\n")
    specific_text = ["\"description\","]
    contains_text_files, does_not_contain_text_files = check_specific_text_in_files(directory, specific_text,
                                                                                    "24-7-15correct")
    print(f"Files containing the text: {contains_text_files}")
    print(f"Files not containing the text: {does_not_contain_text_files}")

    # Files using the editor tag

    print("\n\nEditor:\n")
    specific_text = ["editor"]
    contains_text_files, does_not_contain_text_files = check_specific_text_in_files(directory, specific_text,
                                                                                    "24-7-15ediWrong")
    print(f"Files containing the text: {contains_text_files}")
    print(f"Files not containing the text: {does_not_contain_text_files}")

    # Files using either tag

    print("\n\nEither:\n")
    specific_text = ["editor", "\"description\","]
    contains_text_files, does_not_contain_text_files = check_specific_text_in_files(directory, specific_text,
                                                                                    "24-7-15correct")
    print(f"Files containing the text: {contains_text_files}")
    print(f"Files not containing the text: {does_not_contain_text_files}")


if __name__ == "__main__":
    print_error_file_names()
