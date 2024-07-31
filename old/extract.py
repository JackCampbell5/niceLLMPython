import zipfile, io
from helper_methods.extract_helpers import *

ret_dict = {}

"""Takes files form the online API and exports them ot Azure and the local files"""


def extract_data(offset, limit, instrument, dir_name, ext="", output=True, all=0):
    count = 0
    num = 0
    api = "https://ncnr.nist.gov/ncnrdata/metadata/api/v1/datafiles"
    r = requests.get(api, params={"filename": "%.nxz%", "instrument": instrument, "limit": limit, "offset": offset})
    result = r.json()  # List of dictionary containing the files gotten
    for num in range(len(result)):
        fileinfo = result[num]  # name of this specific file
        file_name = fileinfo["filename"]
        ex_id = fileinfo["experiment_id"]
        start_date = fileinfo["start_date"]
        if ex_id in ret_dict and ret_dict[ex_id] >= 5:
            continue
        elif ex_id in ret_dict:
            ret_dict[ex_id] += 1
        else:
            ret_dict[ex_id] = 1

        # Add file meta data
        meta = (f"file_name: {file_name}, experiment_id: {ex_id}, instrument_name: {instrument},"
                f" start_date: {start_date} \n\n")

        """
        Process a single file after printing out id and name
        ID = experiment id
        name = filename
        """
        # Get contents of a specific file
        data = requests.get(
            f"https://ncnr.nist.gov/pub/ncnrdata/{fileinfo['localdir']}/{fileinfo['filename']}").content

        # Gets the trajectory data from the file
        nxz = zipfile.ZipFile(io.BytesIO(data))

        # If the file does not exist break the loop
        try:
            trajectory_datasets = [d.filename for d in nxz.filelist if
                                   d.filename.endswith("DAS_logs/trajectory/config")]
            file_trajectory = nxz.read(trajectory_datasets[0])
        except IndexError:
            print_error(file_name + " can not be processed and is being skipped (#" + id + ")")
            break

        # Process the trajectory to prepare it to be sent
        file_trajectory = unescape(file_trajectory.decode('utf-8'))
        file_trajectory = meta + file_trajectory[file_trajectory.find("{"):]

        # Create a new file name based on the old one to include an id
        n_name = file_name[:file_name.find('.')] + "(" + ex_id + ")" + file_name[file_name.find('.'):] + ".txt"

        # Get the path to the user's "Documents" folder / extracted files
        documents_folder = os.path.expanduser("~/Documents/extracted_files")

        # Create the path to the desired subfolder within "Documents"
        folder_path = os.path.join(documents_folder, dir_name + ext)

        # Ensure the folder exists, create if it does not
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # If putting all in one file make the name all
        if all != 0:
            # Create the full file path
            n_name = os.path.join(folder_path, f"all{all}.txt")
        else:
            # Check if the file already exists
            if os.path.exists(os.path.join(folder_path, n_name)):
                print_error(n_name + " already exists in " + folder_path)
                continue
                #
                # # Get the current date and time
                # current_time = datetime.now().strftime("(%Y-%m-%d_%H!%M!%S)")
                #
                # # Split the file name into name and extension
                # file_base = n_name[:n_name.find('.')]
                # file_ext = n_name[n_name.find('.'):]
                #
                # # Add the date and time to the file name
                # n_name = f"{file_base}_{current_time}{file_ext}"
        # Update the file path
        file_path = os.path.join(folder_path, n_name)
        if output:
            # Write the data to the file
            with open(file_path, 'a') as file:
                # Add a header for each new file body
                file.write(file_trajectory)
                file.write("\n\n")  # Add spacing between entries
            print(f'{n_name} saved to: {folder_path}')


"""
Methods to grab and process all the files 

NICE API Documentation: 
https://ncnr.nist.gov/ncnrdata/metadata/search/api_docs.html#tag/Experiment/operation/searchExperiments

Instrument options:
bt1, bt2, bt4, bt5, bt7, bt8, bt9, macs, ng1, cg1, hfbs, vsans, dcs, ng5,
 ng7, ng7sans, nse, ngb30sans, ngbsans, ngd, cgd, phades, candor
"""

# Constantly changed params
file_num = 1000  # The number of files to grab
date = "24-6-11"  # The date/name of the folder to name
extension = "b"  # The subfolder if multiple folders made on one day

# Test case parameters
out = True  # Whether the code should output
all = 0

# Not modified often
start_pos = 0  # Where to start grabbing files from
instr = "cgd"  # The instrument to select

for a in range(80):
    start_pos = a * 1000
    print("start_pos: ", start_pos, " ret_dict: ", len(ret_dict), " a:", a)
    extract_data(limit=file_num, offset=start_pos, instrument=instr, dir_name=date, ext=extension, output=out)
