# Helper Methods
Independent files that do a certain action

### [add_text.py](add_text.py)
Takes every file and adds a line to the top of it if the text is not already present

### [count_tokens.py](count_tokens.py)
Counts and prints number of tokens in files. Creating a dictionary of tokenNum:"how many files have that many tokens"
This allows you to get the average of a single file with further calculations.
Also includes information on counting a single file


### [delete_from_list.py](delete_from_list.py)
Takes a list of files and removes them from the specified container in azure and local directory

### [extract_all.py](extract_all.py)
Takes the files form a large file directory, go through every sub folder, take the files and put them into a new folder and put all files with issues in another folder.

### [extract_helpers.py](extract_helpers.py)
+ **CustomEncoder** - Helper class for print to file that encodes json properly
+ **print_error()** - Prints to the console in red
+ **unescape()** - Takes the data and escapes it to format properly
+ **file_num()** - Prints the amount of files in the given directory and all its sub directory's
+ **create_id_dict()** - Creates a dictionary mapping filenames to experiment IDs for a given instrument
+ **print_to_file()** - Prints the provided parameter to a file

### [move_and_remove.py](move_and_remove.py)
Moves all files from the source directory to the destination directory and removes all directories in the source
directory

### [set_meta.py](set_meta.py)
Loops through files in the directory setting the azure meta data based on what is contained in the first line.
Deletes the first line when done.

### [similarity.py](similarity.py)
Reads all the filenames from a doc and finds how similar all of the files in the list are. Makes a directory and
makes a file with the minimum number of files to remove at each threshold.

### [transfer_working.py](transfer_working.py)
Move all files in the list from one container to another in azure and one folder to another locally.

## File Manipulation
Methods for file minipulation that work locally
### [compare_files.py](file_manipulation/compare_files.py)
Takes 2 files containing list of files and compare there contents to see how many different names they have.

### [copy_merge_files.py](file_manipulation/copy_merge_files.py)
Copy file names from the file list from the source directory to the destination directory. Also prints the contents
of the file to a big file.

### [find_error_files.py](file_manipulation/find_error_files.py)
+ **print_error_file_names()**-Checks how many files have the description tag, the editor tag, or both. Prints all
  results to a file.
+ **check_specific_text_in_files()**- Looks through every file in the directory for every element in specific_text.
  Returns a count of the files with and without this text. Also creates a file containing all the file names that were not valid

### [find_extract_text.py](file_manipulation/find_extract_text.py)
Looks through a directory, finds the search_text, and add the line where it is referenced to a file.

### [get_file_info.py](file_manipulation/get_file_info.py)
+ **find_earliest_modified_date()**- Goes through the given directory including all its sub folders, and find the
  earliest file modified date and time
+ **get_num_experiments()**- Gets and returns a dictionary of counts for each experiment number in the directory.
+ **find_file_with_most_lines()**- Finds the file with the most lines in the given directory
+ **find_files_with_least_lines()**- Finds the top 10 files with the least lines and returns an array of them

### [move_list_of_files.py](file_manipulation/move_list_of_files.py)
Move files with file names in the file list from the starting to ending folder, locally .
