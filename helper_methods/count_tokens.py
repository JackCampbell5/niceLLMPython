import os

from token_count import TokenCount

"""
Counts and prints number of tokens in files. Creating a dictionary of tokenNum:"how many files have that many tokens" 
This allows you to get the average of a single file with further calculations.
Also includes information on counting a single file
"""


def token_count_directory(directory):
    ret_dict = []
    for file in os.listdir(directory):
        new_dir = os.path.join(directory, file)
        tokens = tc.num_tokens_from_file(new_dir)
        if tokens in ret_dict:
            ret_dict[tokens] += 1
        else:
            ret_dict[tokens] = 1
    return ret_dict


if __name__ == "__main__":
    tc = TokenCount(model_name="gpt-4o")
    tokens = tc.num_tokens_from_file(os.path.expanduser("~/PycharmProjects/niceLLM/chat_bot/system_message.txt"))
    print(f"System Message tokens:{tokens}")
    directory = os.path.expanduser("~/Documents/niceLLM/output/Correct(Errors)")
    print(f"Token Dictionary:{token_count_directory(directory)}")
