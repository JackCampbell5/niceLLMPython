import os, sys,requests


def print_error(message):
    print(message, file=sys.stderr)


"""
Takes the data and escapes it to format properly 
"""


def unescape(data):
    output = data.replace('\\\\', '\1') \
        .replace('\\t', '\t') \
        .replace('\\r', '\r') \
        .replace('\\n', '\n') \
        .replace('\1', '\\') \
        .replace('\\u0027', "'")
    return output


def file_num(directory):
    len([name for name in os.listdir(os.path.expanduser(directory)) if os.path.isfile(os.path.join(directory, name))])


def create_id_dict(instrument):
    ret_dict = {}
    api = "https://ncnr.nist.gov/ncnrdata/metadata/api/v1/datafiles"
    r = requests.get(api, params={"filename": "%.nxz%", "instrument": instrument, "limit": 2500, "offset": 0})
    result = r.json()  # List of dictionary containing the files gotten
    for num in range(len(result)):
        fileinfo = result[num]  # name of this specific file
        ret_dict[fileinfo["filename"]] = fileinfo["experiment_id"]
    return ret_dict