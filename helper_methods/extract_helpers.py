import json
import os, sys, requests
import shutil, time
from typing import Any
import token_count

from openai.types.chat.chat_completion import ChatCompletionMessage, Choice
from token_count import TokenCount


class CustomEncoder(json.JSONEncoder):
    """
    Helper class for print to file that encodes json properly
    """
    def default(self, obj: Any) -> Any:
        if isinstance(obj, Choice):
            return {
                'finish_reason': obj.finish_reason,
                'index': obj.index,
                'logprobs': obj.logprobs,
                'message': {
                    'content': obj.message.content,
                    'role': obj.message.role,
                    'function_call': obj.message.function_call,
                    'tool_calls': obj.message.tool_calls,
                    'end_turn': obj.message.end_turn,
                    'context': obj.message.context
                }
            }
        if isinstance(obj, ChatCompletionMessage):
            return {
                'content': obj.content,
                'role': obj.role,
                'function_call': obj.function_call,
                'tool_calls': obj.tool_calls,
                'end_turn': obj.end_turn,
                'context': obj.context
            }


def print_error(message):
    """
    Prints to the console in red
    :param message: The message to print
    :return: None
    """
    print(message, file=sys.stderr)


def unescape(data):
    """
    Takes the data and escapes it to format properly
    """
    output = data.replace('\\\\', '\1') \
        .replace('\\t', '\t') \
        .replace('\\r', '\r') \
        .replace('\\n', '\n') \
        .replace('\1', '\\') \
        .replace('\\u0027', "'")
    return output


def file_num(directory):
    """
    Prints the amount of files in the given directory and all its sub directory's
    :param directory: The directory to search
    :return: The number of how many files
    """
    return len([name for name in os.listdir(os.path.expanduser(directory)) if os.path.isfile(os.path.join(directory,
                                                                                                      name))])


def create_id_dict(instrument):
    """
    Creates a dictionary mapping filenames to experiment IDs for a given instrument
    :param instrument: Name of the instrument
    :return: Dictionary with filenames as keys and experiment IDs as values
    """
    ret_dict = {}
    api = "https://ncnr.nist.gov/ncnrdata/metadata/api/v1/datafiles"
    r = requests.get(api, params={"filename": "%.nxz%", "instrument": instrument, "limit": 2500, "offset": 0})
    result = r.json()  # List of dictionary containing the files gotten
    for num in range(len(result)):
        fileinfo = result[num]  # name of this specific file
        ret_dict[fileinfo["filename"]] = fileinfo["experiment_id"]
    return ret_dict


def print_to_file(file_path, file_name, what_to_print, type_print="str", overwrite=False):
    """
    Prints the provided parameter to a file
    :param file_path: Path to the directory where the file will be saved
    :param file_name: Name of the file to be saved
    :param what_to_print: Content to be printed to the file
    :param type_print: Type of the content to print ("str", "json", "arr")
    :param overwrite: Boolean flag to indicate whether to overwrite the file if it exists
    :return: None
    """
    file_name = file_name + ".txt"
    updated_file_name = file_name
    if not overwrite:
        num = 0
        while os.path.exists(os.path.join(file_path, updated_file_name)):
            start = file_name[:file_name.rfind(".")]
            end = file_name[file_name.rfind("."):]
            updated_file_name = start + f"({num})" + end
            num += 1
    if type_print == "json":
        content = json.dumps(what_to_print, indent=4, cls=CustomEncoder)
    elif type_print == "arr":
        content = ""
        for element in what_to_print:
            content += str(element) + "\n"
    else:
        content = what_to_print
    with open(os.path.join(file_path, updated_file_name), 'w') as file:
        file.write(content)
    print(f"Content written to {file_name}")


if __name__ == "__main__":
    pass

