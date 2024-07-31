import os


def find_and_extract_text(directory, search_text, output_file, not_text=None, whole_file=False):
    """
    Looks through a directory, finds the search_text, and add the line where it is referenced to a file.
    :param directory: The directory to search in
    :param search_text: The text to search for
    :param output_file: The name of the file to save the results(Auto one directory up)
    :param not_text: Text you want the same line as search text to not include
    :param whole_file: If false prints single line it was referenced at if true prints the entrie file
    :return: The a string containing the number searched and the number found
    """
    count = 0
    results = ""

    # Check if the directory exists and is a directory
    if not os.path.exists(directory):
        print(f"Error: The directory '{directory}' does not exist.")
        return
    if not os.path.isdir(directory):
        print(f"Error: The path '{directory}' is not a directory.")
        return  # Open the output file in write mode

    output_path = os.path.join(os.path.dirname(directory), output_file)

    with open(output_path, 'w') as output:
        # Loop through all files in the specified directory
        all_files = os.listdir(directory)
        for filename in all_files:
            print(filename)
            # Get the full path of the file
            file_path = os.path.join(directory, filename)

            # Check if it's a file (not a directory)
            if os.path.isfile(file_path):
                # Open and read the file
                with open(file_path, 'r') as file:
                    str1 = file.readlines()
                    found = False
                    for content in str1:
                        if not found:
                            # Find the position of the search text
                            index = content.find(search_text)
                            not_index = -1
                            if not_text is not None:
                                not_index = content.find(not_text)
                            if index != -1 and not_index == -1:
                                count += 1
                                # Extract the text that follows the search text
                                # extracted_text = content[index + len(search_text):]

                                # Write the filename and the extracted text to the output file
                                output.write(f"\nFile: {filename}\n\n")
                                if whole_file:
                                    for line in str1:
                                        output.write(line + "\n")
                                else:
                                    output.write(content + "\n")
                                output.write("-" * 40 + "\n")
                                found = True
        results = f"Total searched: {len(all_files)}\nTotal found:{str(count)}"
        output.write(results)
        print(f"File {output_file} correctly output to {output_path}")
    return results


if __name__ == "__main__":
    directory = os.path.expanduser("~/Documents/niceLLM/output/Correct")  # Where all the files are
    find_and_extract_text(directory, "description", os.path.join(directory, "output.txt")
                          , not_text=None, whole_file=False)
