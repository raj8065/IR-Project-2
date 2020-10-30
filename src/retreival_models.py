import math


class retreival_model():

    def __init__(self, doc_num, data, documents):
        self.data = data
        self.documents = documents
        self.doc_num = doc_num  # Number of documents
        self.document_with_term_occurrences = dict()  # Cache so calculations can be done quicker

    # Returns the total number of documents AKA N
    def get_number_of_documents(self):
        return self.doc_num

    # TODO change depending on datamodel
    # Returns a list of all the documents
    def get_all_documents(self):
        return self.documents

    # TODO change depending on datamodel
    # Returns all of the documents for a term
    def get_documents_for_term(self, term):
        return self.data[term]

    # TODO change depending on datamodel
    # Returns the number of occurrences of the term in the document AKA f_ik
    def get_number_of_term_in_document(self, term, doc):
        return self.data[term][doc]

    # Returns the number of documents in which the term appears AKA n_k
    def get_number_of_document_with_term(self, term):
        if term in self.document_with_term_occurrences:
            return self.document_with_term_occurrences[term]

        sum = 0
        for doc in self.get_documents_for_term(term):
            sum = sum + 1
        self.document_with_term_occurrences[term] = sum

        return sum


class tf_idf_model(retreival_model):

    # Generates the ranks for all the documents
    def generate_tf_idf_ranks(self, query_words):
        ranks = []
        for doc in self.get_all_documents():
            ranks.append(self.generate_tf_idf_rank(query_words, doc))
        return ranks

    # Generates a rank for a single document
    def generate_tf_idf_rank(self, query_words, doc):
        denominator = self.generate_tf_idf_term_rank_denominator(self, doc)
        sum = 0
        for word in query_words:
            sum = sum + self.generate_tf_idf_term_rank(word, doc, denominator)
        return sum

    # Generates the tf_idf rank for a term - doc pair
    def generate_tf_idf_term_rank(self, term, doc, denominator):
        return self.generate_tf_idf_term_rank_numerator(self, doc, term) / denominator

    # Generates the numerator of the tf_idf rank for a term - doc pair
    def generate_tf_idf_term_rank_numerator(self, doc, term):
        N = self.get_number_of_documents()
        n_k = self.get_number_of_document_with_term(term)
        f_ik = self.get_number_of_term_in_document(term, doc)

        return (math.log10(f_ik) + 1.0) * math.log10(N/n_k)

    # Generates the denominator of the tf_idf rank for a term - doc pair
    def generate_tf_idf_term_rank_denominator(self, query_words, doc):
        N = self.get_number_of_documents()
        total = 0.0
        for word in query_words:
            n_k = self.get_number_of_document_with_term(word)
            f_ik = self.get_number_of_term_in_document(word, doc)

            total = total + math.pow((math.log10(f_ik) + 1.0) * math.log10(N/n_k), 2)
        return math.sqrt(total)