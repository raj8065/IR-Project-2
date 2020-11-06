from src import index_files

from src.retreival_models import BM25Model
from src.retreival_models import TfIdfModel


from src.retreival_models import *


def get_inverted_index():
    return []

def get_doc_lookup():
    return []

def generate_search_results(rankings, filename):
    return None

def main():

    inv_index = get_inverted_index()
    doc_lookup = get_doc_lookup()

    BM25_model = BM25Model(inv_index, doc_lookup)
    TF_IDF_model = TfIdfModel(inv_index, doc_lookup)

    query = input("Enter Query (Input 'quit' to stop): ").strip()
    while query != "quit":
        query_parts = index_files.clean_input(query)

        BM25_rankings = BM25_model.generate_ranks(query_parts)
        TF_IDF_rankings = TF_IDF_model.generate_ranks(query_parts)

        generate_search_results(BM25_rankings, "BM25_results.html")
        generate_search_results(TF_IDF_rankings, "TF_IDF_results.html")

        query = input("Enter Query (Input 'quit' to stop): ").strip()

if __name__ == "__main__":
    main()