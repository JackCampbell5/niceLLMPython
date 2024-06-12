from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import os, tempfile
from extractTraj.extract_helpers import print_error, create_id_dict

# Constants
STORAGE_ACCOUNT_NAME = "nicellmstorage"
ACCOUNT_KEY = os.getenv("AZURE_OPENAI_API_KEY")
CONTAINER_NAME = "trajectories"
count_max = 0

# Connection string connection_string = f"DefaultEndpointsProtocol=https;AccountName={
# STORAGE_ACCOUNT_NAME};AccountKey={ACCOUNT_KEY};EndpointSuffix=core.windows.net"
connection_string = ("DefaultEndpointsProtocol=https;AccountName=nicellmstorage;AccountKey=x"
                     "/fdM3T0wJxmrjf0ihIkqjSRXpk3fnACnRfjHZOeJxZififUrXgz8W5L5FlQ/JTs1ChMRHyqru4y+ASthh9JZg"
                     "==;EndpointSuffix=core.windows.net")

# Create the BlobServiceClient object
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)

# File path
blob_list = container_client.list_blobs()

# # All ID's
# id_dict = create_id_dict("cgd")

# Temporary directory to download blobs
with tempfile.TemporaryDirectory() as temp_dir:
    count = 0
    for blob in blob_list:
        # if count > count_max:
        #     break
        # count += 1

        try:
            blob_client = container_client.get_blob_client(blob)

            # Download the blob to a temporary file
            download_file_path = os.path.join(temp_dir, blob.name)
            with open(download_file_path, "wb") as download_file:
                download_file.write(blob_client.download_blob().readall())

            # Read parameters from the file content
            with open(download_file_path, "r") as file:

                lines = file.readlines()
                if len(lines) < 2:
                    print(f"File {blob.name} does not contain enough lines for metadata.")
                    continue
                # Assuming the first line contains year, month, day in this format: year=2023;month=06;day=11
                first_line = lines[0].strip()
                try:
                    # Parse metadata using ',' and ': '
                    params = {}
                    for param in first_line.split(', '):
                        key, value = param.split(':', 1)
                        params[key.strip()] = value.strip()
                    # Extract specific metadata fields
                    file_name = params.get("file_name")
                    experiment_id = params.get("experiment_id")
                    instrument_name = params.get("instrument_name")
                    start_date = params.get("start_date")

                except ValueError as e:
                    print_error(f"Error parsing first file line metadata trying pre existing data in {blob.name} ")
                    try:
                        # Fetch and print metadata
                        blob_properties = blob_client.get_blob_properties()
                        file_name = blob_properties.metadata.get("file_name")
                        experiment_id = blob_properties.metadata.get("experiment_id")
                        instrument_name = blob_properties.metadata.get("instrument_name")
                        start_date = blob_properties.metadata.get("start_date")
                    except ValueError as e:
                        print_error(f"Pre existing data does not exist in {blob.name} skipping file")
                        continue

                if file_name and experiment_id and instrument_name and start_date:
                    # Write the remaining lines back to the file
                    with open(download_file_path, "w") as file:
                        if "JSON file" in lines[1] and "JSON file" in lines[0]:
                            lines.pop(1)
                        if "JSON file" not in lines[0]:
                            if "\n" not in lines[1]:
                                lines = ["", ""] + lines
                            lines[1] = "This is a JSON file containing a trajectory for the MAGIK instrument \n"
                            file.writelines(lines[1:])  # Remove the first two lines
                        else:
                            file.writelines(lines)

                # Re-upload the modified file and set metadata
                    with open(download_file_path, "rb") as file_stream:
                        blob_client.upload_blob(file_stream, overwrite=True)

                        # Set metadata
                        metadata = {
                            "file_name": file_name,
                            "experiment_id": experiment_id,
                            "instrument_name": instrument_name,
                            "start_date": start_date
                        }
                        blob_client.set_blob_metadata(metadata)

                        # Fetch and print metadata
                        blob_properties = blob_client.get_blob_properties()
                        file_name_from_blob = blob_properties.metadata.get("file_name")
                        experiment_id_from_blob = blob_properties.metadata.get("experiment_id")
                        instrument_name_from_blob = blob_properties.metadata.get("instrument_name")
                        start_date_from_blob = blob_properties.metadata.get("start_date")

                        print(f"SET:  {blob.name} ({file_name_from_blob}, {experiment_id_from_blob},"
                              f" {instrument_name_from_blob}, {start_date_from_blob})")
                else:
                    print_error(f"File {blob.name} does not contain valid metadata.")
        except FloatingPointError as e:
            print_error(f"An error occurred: {e} \n In file {blob.name}")
