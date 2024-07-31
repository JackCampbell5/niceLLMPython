import os
import shutil

from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from extract_helpers import print_error

"""
Move all files in the list from one container to another in azure and one folder to another locally.
"""

# Azure Blob Storage connection string
connection_string = os.getenv("AZURE_STORAGE_CONNECT")

# Source and destination container names
source_container = "moretrajectories"
destination_container = "7-16trajectories"

# Source and destination directories for local files
source_dir = os.path.expanduser("~/Documents/niceLLM/output/Correct")
destination_dir = os.path.join(os.path.dirname(source_dir), "MoreCorrect")

# Path to the txt file containing the list of filenames
FILENAME_LIST_PATH = os.path.expanduser("~/Documents/niceLLM/output/24-7-15correct.txt")


def move_blob(blob_service_client, blob_name):
    # Get the source blob client
    source_blob = blob_service_client.get_blob_client(container=source_container, blob=blob_name)

    # Download the blob content
    blob_data = source_blob.download_blob().readall()

    # Get the destination blob client
    destination_blob = blob_service_client.get_blob_client(container=destination_container, blob=blob_name)

    # Upload the blob content to the destination container
    destination_blob.upload_blob(blob_data)

    # Delete the source blob
    source_blob.delete_blob()


def move_local_file(filename):
    # Construct full file paths
    source_path = os.path.join(source_dir, filename)
    destination_path = os.path.join(destination_dir, filename)

    # Move the file
    shutil.move(source_path, destination_path)


def main():
    # Create the BlobServiceClient object
    blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)

    # Read the list of filenames from the txt file
    with open(FILENAME_LIST_PATH, 'r') as file:
        filenames = file.readlines()

    # Strip any whitespace characters like `\n` at the end of each line
    filenames = [filename.strip() for filename in filenames]

    # Move each file from the source container to the destination container
    for filename in filenames:
        print(filename)
        try:
            move_blob(blob_service_client, filename)
            move_local_file(filename)
            print(f"Moved: {filename}")
        except Exception as e:
            print_error(filename + "already exists")


if __name__ == "__main__":
    main()
