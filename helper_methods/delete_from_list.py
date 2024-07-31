from azure.storage.blob import BlobServiceClient
import os
from extract_helpers import print_error

"""
Takes a list of files and removes them from the specified container in azure and local directory
"""

# Define the connection string to your Azure Blob Storage account
CONTAINER_NAME = "moretrajectories"
connection_string = os.getenv("AZURE_STORAGE_CONNECT")
# Access with
remove_too = os.path.expanduser("~/Documents/niceLLM/output/correct")
file_list = os.path.expanduser("~/Documents/niceLLM/output/output_names.txt")

# Initialize the BlobServiceClient
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)

# Read the list of files to delete from the text file
with open(file_list, 'r') as file:
    files_to_delete = file.readlines()

# Remove any whitespace characters, like newlines
files_to_delete = [file.strip() for file in files_to_delete]

# Iterate through the list and delete each file
num = 0
for file_name in files_to_delete:
    try:
        blob_client = container_client.get_blob_client(file_name)  # Get the blob client for the file
        os.remove(os.path.join(remove_too, file_name))  # Remove the file from the local directory
        blob_client.delete_blob()  # Delete the file from the Azure container
        num += 1
        print(f"Deleted: {file_name}")  # Print the name of the deleted file
    except Exception as e:
        print_error(f"Failed to delete {file_name}: {e}")  # Print an error message if deletion fails
print(f"Files successfully deleted: {num}")  # Print the number of successfully deleted files
print("Deletion process completed.")  # Print a message indicating the completion of the process
