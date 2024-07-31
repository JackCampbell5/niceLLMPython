from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import os
from extract_helpers import print_error

"""
Takes every file and adds a line to the top of it if the text is not already present
"""

# Define your connection string and container name
CONTAINER_NAME = "moretrajectories"
connection_string = os.getenv("AZURE_STORAGE_CONNECT")

# Initialize the BlobServiceClient
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Get a ContainerClient
container_client = blob_service_client.get_container_client(CONTAINER_NAME)

# List all blobs in the container
blobs_list = container_client.list_blobs()

# Directory containing the files to be processed
directory = os.path.expanduser("~/Documents/niceLLM/output/AllFiles")

# Iterate over each file in the directory
for file_name in os.listdir(directory):
    # Get the blob client
    blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=file_name)

    # Construct the file path
    get_path = os.path.join(directory, file_name)

    # Read the file content
    content = None
    with open(get_path, 'r') as file:
        content = file.read()

    # Extract the instrument name from the file name
    inst_name = file_name[:file_name.find("(")]

    # Check if the file content is empty
    if content is None or content.strip() == "":
        print_error(f"{file_name} can not be correctly processed")
        continue

    # Check if the file has already been processed
    if "This is a JSON file " in content:
        print_error(f"{file_name} already processed")
        continue

    # Add the specified line to the top of the file content
    content = f"This is a JSON file containing a trajectory for the {inst_name} instrument \n" + content

    # Write the modified content back to the file
    with open(get_path, 'w') as file:
        file.write(content)

    # Upload the modified content back to the blob
    blob_client.upload_blob(content, overwrite=True)
    print(file_name)

print("All text files have been processed.")
