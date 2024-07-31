# Nice Large Language Model


## Setup:
1. pip install -r requirements.txt
2. Set up environment variables 

## Set up environment variables 
1. Follow the guide in the google drive folder
2. setx AZURE_STORAGE_CONNECT "connection String"
   + Get on Azure at nicellmstoarge / access keys /connection string


# [Chat](chat_bot)
Python version of the NICE LLM
+ To run, run chat_interact.py 
+ Test files- Loops through for testing purposes, with different prompts to check success 


# [Helper Methods](helper_methods)
Independent files that do a certain action
+ [add_text.py](helper_methods/add_text.py)
+ [count_tokens.py](helper_methods/count_tokens.py)
+ [delete_from_list.py](helper_methods/delete_from_list.py)
+ [extract_all.py](helper_methods/extract_all.py)
+ [extract_helpers.py](helper_methods/extract_helpers.py)
+ [move_and_remove.py](helper_methods/move_and_remove.py)
+ [set_meta.py](helper_methods/set_meta.py)
+ [similarity.py](helper_methods/similarity.py)
+ [transfer_working.py](helper_methods/transfer_working.py)
## File Manipulation
Methods for file manipulation that work locally
+ [compare_files.py](helper_methods/file_manipulation/compare_files.py)
+ [copy_merge_files.py](helper_methods/file_manipulation/copy_merge_files.py)
+ [find_error_files.py](helper_methods/file_manipulation/find_error_files.py)
+ [find_extract_text.py](helper_methods/file_manipulation/find_extract_text.py)
+ [get_file_info.py](helper_methods/file_manipulation/get_file_info.py)
+ [move_list_of_files.py](helper_methods/file_manipulation/move_list_of_files.py)

# [Old(Not in use) Files](old)
+ [extract.py](old/extract.py)
+ [check_exist.py](old/check_exist.py)


newVersionUpdate to update if model or other updates are made in azure 
