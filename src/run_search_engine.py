import csv
import os
import ast

from src import index_files
from src.retreival_models import BM25Model
from src.retreival_models import TfIdfModel

from src.retreival_models import *


# Gets the inverted index created by index_files.gen_index
def get_inverted_index(rel_path):
    inverted_index = {}
    doc_lookup_file = os.path.join(os.path.dirname(os.getcwd()) + "\\" + rel_path)
    with open(doc_lookup_file, 'r') as f:
        idx_data = csv.reader(f, delimiter="\t")
        for row in idx_data:
            if not row:
                # weed out empty rows
                continue

            inverted_index[row[0]] = [ast.literal_eval(row[1]), row[2], row[3] ]

    return index_files.gen_index("res/out")

# Gets the document lookup created by html_parser.write_doc_table_to_tsv
def get_doc_lookup(rel_path):
    return index_files.get_doc_lookup_table(rel_path)

# TODO Generate a html file for search results
def generate_search_results(rankings, filename):
    return None


def main():

    inv_index = get_inverted_index("res\\inverted_index.tsv")
    doc_lookup = get_doc_lookup("res\\doc_lookup.tsv")

    BM25_model = BM25Model(inv_index, doc_lookup)
    TF_IDF_model = TfIdfModel(inv_index, doc_lookup)

    query = input("Enter Query (Input 'quit' to stop): ").strip()
    while query != "quit":
        query_parts = index_files.clean_input(query)

        BM25_rankings = BM25_model.generate_ranks(query_parts)
        TF_IDF_rankings = TF_IDF_model.generate_ranks(query_parts)

        print(BM25_rankings)
        print(TF_IDF_rankings)

        generate_search_results(BM25_rankings, "BM25_results.html")
        generate_search_results(TF_IDF_rankings, "TF_IDF_results.html")

        query = input("Enter Query (Input 'quit' to stop): ").strip()


if __name__ == "__main__":
    main()
