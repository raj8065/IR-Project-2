import csv
import os
import ast

import index_files
from retreival_models import BM25Model
from retreival_models import TfIdfModel
from tsv_reader import Tsv_Reader
from retreival_models import *

# TODO Generate a html file for search results
def generate_search_results(rankings, filename):
    return None


def print_results(results_dict, n_hits, doc_lookup):
    results_sorted = sorted(results_dict.items(), key=lambda x: x[1], reverse=True)
    ctr_hits = 0
    for item in results_sorted:
        if ctr_hits == n_hits or item[1] == 0:
            break
        print(doc_lookup[item[0]].get("file_name"))
        ctr_hits = ctr_hits + 1

def main():

    tsv_reader = Tsv_Reader("res\\doc_lookup.tsv", "res\\inverted_index.tsv")
    inv_index = tsv_reader.get_inv_idx()
    doc_lookup = tsv_reader.get_doc_lookup_table()

    BM25_model = BM25Model(inv_index, doc_lookup)
    TF_IDF_model = TfIdfModel(inv_index, doc_lookup)

    query = input("Enter Query (Input 'quit' to stop): ").strip()
    while query != "quit":
        query_parts = index_files.clean_input(query)

        BM25_rankings = BM25_model.generate_ranks(query_parts)
        TF_IDF_rankings = TF_IDF_model.generate_ranks(query_parts)

        print("BM_25 Rankings: ")
        print_results(BM25_rankings, 60, doc_lookup)
        print("\nTF-IDF Rankings: ")
        print_results(TF_IDF_rankings, 60, doc_lookup)

        generate_search_results(BM25_rankings, "BM25_results.html")
        generate_search_results(TF_IDF_rankings, "TF_IDF_results.html")

        query = input("Enter Query (Input 'quit' to stop): ").strip()


if __name__ == "__main__":
    main()
