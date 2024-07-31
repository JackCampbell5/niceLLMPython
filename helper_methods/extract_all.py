import os
from typing import LiteralString

from azure.storage.blob import BlobServiceClient
import shutil
from extract_helpers import print_error

"""
Takes the files form a large file directory, go through every sub folder, take the files and put them into a new 
folder and put all files with issues in another folder. 
"""


# Function to copy a file with a unique name if the file already exists in the destination
def copy_file(copy_file_path, file_name) -> LiteralString | str | bytes:
    updated_file_name = file_name
    num = 0
    while os.path.exists(os.path.join(copy_file_path, updated_file_name)):
        start = file_name[:file_name.rfind(".")]
        end = file_name[file_name.rfind("."):]
        updated_file_name = start + f"({num})" + end
        num += 1
    if num > 10:
        print_error(f"Error with {file_name} in {copy_file_path} {num}")
    return os.path.join(copy_file_path, updated_file_name)


# Function to save a file and upload it to Azure Blob Storage
def save_file(path):
    try:
        if len(path_arr) > 2 and path_arr[2] not in secondary_folders:
            new_file_name = f"{path_arr[0]} ({path_arr[1]})({path_arr[2]}){path_arr[len(path_arr) - 1]}"
        else:
            new_file_name = path_arr[0] + "(" + path_arr[1] + ")" + path_arr[len(path_arr) - 1]
        new_file_name = new_file_name.replace(" ", "")
        location_saved = shutil.copy2(path, copy_file(correct_folder, new_file_name))
        saved_file_name = location_saved[location_saved.rfind("\\") + 1:]
        print("File Saved", saved_file_name)

        # Create a blob client
        # blob_client = container_client.get_blob_client(saved_file_name)

        # Upload the file to Azure Blob Storage
        # with open(path, "rb") as data:
        # blob_client.upload_blob(data, overwrite=True)

        # Set metadata
        metadata = {
            "file_name": path_arr[len(path_arr) - 1],
            "experiment_id": path_arr[0],
            "instrument_name": path_arr[1],
            # "start_date": start_date
        }
        if len(path_arr) > 2 and path_arr[2] not in secondary_folders:
            metadata["extra_folder"] = path_arr[2]
        else:
            metadata["extra_folder"] = None

        # Set metadata for the blob
        # blob_client.set_blob_metadata(metadata)
        os.remove(path)
        print("File Uploaded", saved_file_name)
    except Exception as e:
        print_error(path)


# Function to create directories for issue files
def create_dir():
    if len(path_arr) > 0:
        issue_path = os.path.join(issue_folder, path_arr[0])
        if not os.path.exists(issue_path):
            os.mkdir(issue_path)
        ret_str = ""
        for num in range(len(path_arr) - 1):
            ret_str += path_arr[num + 1]
        return os.path.join(path_arr[0], ret_str)
    else:
        return ""


# Recursive function to process directories and files
def new_method(new_path, num, checks=True):
    if os.path.isdir(new_path):
        for deeper_path in os.listdir(new_path):
            path_arr.append(deeper_path)
            new_method(os.path.join(new_path, deeper_path), num + 1, checks=checks)
            path_arr.pop()
    else:
        if len(path_arr) > 2:
            save_file(new_path)
        else:
            print_error(f"Error in {new_path} instrument id is not a directory")
            shutil.copy2(new_path, copy_file(issue_folder, create_dir()))
            os.remove(new_path)


if __name__ == "__main__":
    # Azure storage connection string
    CONTAINER_NAME = "moretrajectories"
    connection_string = os.getenv("AZURE_STORAGE_CONNECT")
    # Define paths
    path_arr = []
    initial_path = os.path.expanduser("~/Documents/niceLLM/")
    input_folder = os.path.join(initial_path, "trajectories")
    output_folder = os.path.join(initial_path, "Output")
    issue_folder = os.path.join(output_folder, "Issue")
    correct_folder = os.path.join(output_folder, "Correct")

    # Create output directories if they do not exist
    for n in [output_folder, issue_folder, correct_folder]:
        if not os.path.exists(n):
            os.mkdir(n)

    # Create the BlobServiceClient object
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    # Create the container client
    container_client = blob_service_client.get_container_client(CONTAINER_NAME)

    file_name = experiment_id = instrument_name = start_date = ""
    secondary_folders = ["trajectories", "Trajectories"]
    num_top = 1
    new_method(input_folder, 0)
