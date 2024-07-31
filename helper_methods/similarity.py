import collections
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict
import networkx as nx
from extract_helpers import print_to_file

"""
Reads all the filenames from a doc and finds how similar all of the files in the list are. Makes a directory and 
makes a file with the minimum number of files to remove at each threshold.
"""


def read_filenames(file_path):
    """Reads a list of filenames from a text file."""
    with open(file_path, 'r') as file:
        filenames = [line.strip() for line in file]
    return filenames


def read_files(file_list, directory):
    """Reads the content of each file in the file_list from the given directory."""
    file_contents = []
    for file_name in file_list:
        file_path = os.path.join(directory, file_name)
        with open(file_path, 'r') as file:
            file_contents.append(file.read())
    return file_contents


def calculate_similarity(file_contents):
    """Calculates the cosine similarity scores between the contents of the files."""
    vectorizer = TfidfVectorizer().fit_transform(file_contents)
    vectors = vectorizer.toarray()
    similarity_matrix = cosine_similarity(vectors)
    return similarity_matrix


def find_identical_files(similarity_matrix, filenames, more_than=1.0):
    """Finds pairs of files with a similarity score of 1 and determines the minimum number of files to remove to avoid duplicates."""
    identical_pairs = []
    for i in range(len(filenames)):
        for j in range(i + 1, len(filenames)):
            if similarity_matrix[i][j] >= more_than:
                identical_pairs.append((filenames[i], filenames[j]))

    # Create a graph where each node is a file and an edge exists between identical files
    G = nx.Graph()
    G.add_edges_from(identical_pairs)

    # Find the minimum vertex cover
    min_vertex_cover = nx.algorithms.approximation.min_weighted_vertex_cover(G)

    return identical_pairs, min_vertex_cover


def help_arr(arr):
    ret_str = "\n" + "-" * 50 + "\n"
    if type(arr) is dict:
        for key, value in arr.items():
            ret_str += f"\n {key}: {str(value)}"
    else:
        for element in arr:
            ret_str += "\n" + str(element)
    return ret_str


if __name__ == "__main__":
    num = 2
    threshold = 0.2
    filenames_path = os.path.expanduser("~/Documents/niceLLM/output/24-7-3ediWrong.txt")
    all_counts_path = os.path.expanduser("~/Documents/niceLLM/output/24-7-24allCounts.txt")
    similarity_count_path = os.path.expanduser("~/Documents/niceLLM/output/24-7-24simCounts.txt")
    directory = os.path.expanduser("~/Documents/niceLLM/output/Correct(Errors)")

    filenames = read_filenames(filenames_path)
    print("Filenames")
    file_contents = read_files(filenames, directory)
    print("file_contents")
    similarity_scores = calculate_similarity(file_contents)
    print("similarity_scores")

    with open(all_counts_path, 'a') as file:
        while threshold >= 0.0:
            identical_pairs_loop, min_vertex_cover_loop = find_identical_files(similarity_scores, filenames,
                                                                               more_than=threshold)
            retStr = ""
            retStr += (f"Minimum:{len(min_vertex_cover_loop)}, Identical"
                       f":{len(identical_pairs_loop)}")
            file.write(f"Num:{threshold} {retStr}\n")
            retStr += f"\n\n\nMinimum Files to Remove:{help_arr(min_vertex_cover_loop)}"
            # retStr += f"\n\n\nIdentical Pairs:{help_arr(identical_pairs_loop)}"
            print_to_file(os.path.dirname(directory), f"24-7-3Similarity{threshold}", retStr, "str", overwrite=True)
            threshold -= 0.05
        similarity_count = defaultdict(int)

        for i in range(len(filenames)):
            print(i)
            for j in range(i + 1, len(filenames)):
                threshold = round(similarity_scores[i][j] * 100)
                similarity_count[threshold] += 1
        similarity_count = dict(similarity_count)
        myKeys = list(similarity_count.keys())
        myKeys.sort()
        similarity_count_loop = {i: similarity_count[i] for i in myKeys}

        retStr = ""
        retStr += f"Similarity:{len(similarity_count_loop)}"
        retStr += f"\n\n\nSimilarity Count:{help_arr(similarity_count_loop)}"
        file.write("\n\n\n" + retStr)
        print("Content written to", all_counts_path[all_counts_path.rfind("\\"):])
