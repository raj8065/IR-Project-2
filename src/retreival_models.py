import math

class RetrievalModel():

    def __init__(self, data, documents):
        self.inv_index = data
        self.doc_posting = documents
        self.doc_num = len(documents)  # Number of documents

    # Returns the total number of documents AKA N
    def get_number_of_documents(self):
        return self.doc_num

    # Returns a list of all the documents
    def get_all_documents(self):
        return self.doc_posting.keys()

    # Returns all of the documents for a term
    def get_documents_for_term(self, term):
        posting = self.inv_index.get(term)
        if posting is None:
            return []
        return posting.posting_list.keys()

    # Returns the number of occurrences of the term in the document AKA f_ik
    def get_number_of_term_in_document(self, term, doc):
        posting = self.inv_index.get(term)
        if posting is None:
            return 0
        amnt = self.inv_index[term].posting_list.get(doc)
        if amnt is None:
            return 0
        return amnt

    # Returns the number of documents in which the term appears AKA n_k
    def get_number_of_document_with_term(self, term):
        return len(self.get_documents_for_term(term))

    # Generates the ranks for all the documents AKA the main workhorse of the class
    def generate_ranks(self, query_words):
        ranks = dict()
        for doc in self.get_all_documents():
            ranks[doc] = self.generate_rank(query_words, doc)
        return ranks

    # Generates a rank for a single document
    def generate_rank(self, query_words, doc):
        raise Exception('RetreivalModel superclass used to create a rank.')


class TfIdfModel(RetrievalModel):

    def __init__(self, data, documents):
        super().__init__(data, documents)

    # Generates a rank for a single document
    def generate_rank(self, query_words, doc):

        denominator = self.generate_tf_idf_term_rank_denominator(query_words, doc)
        # If None of the query terms appear in any document then the rank is zero
        if denominator == 0:
            return 0

        rank_sum = 0
        for word in query_words:
            rank_sum += self.generate_tf_idf_term_rank(word, doc, denominator)
        return rank_sum

    # Generates the tf_idf rank for a term - doc pair
    def generate_tf_idf_term_rank(self, term, doc, denominator):
        return self.generate_tf_idf_term_rank_numerator(doc, term) / denominator

    # Generates the numerator of the tf_idf rank for a term - doc pair
    def generate_tf_idf_term_rank_numerator(self, doc, term):
        f_ik = self.get_number_of_term_in_document(term, doc)

        # If the term does not appear in the document, no term weight is added
        if f_ik != 0:
            N = self.get_number_of_documents()
            n_k = self.get_number_of_document_with_term(term)
            return (math.log10(f_ik) + 1.0) * (math.log10(N/n_k))
        else:
            return 0

    # Generates the denominator of the tf_idf rank for a term - doc pair
    def generate_tf_idf_term_rank_denominator(self, query_words, doc):
        N = self.get_number_of_documents()
        total = 0.0
        for word in query_words:
            f_ik = self.get_number_of_term_in_document(word, doc)
            # If the term does not appear in the document, no term weight is added
            if f_ik != 0:
                n_k = self.get_number_of_document_with_term(word)
                total = total + math.pow((math.log10(f_ik) + 1.0) * (math.log10(N/n_k)), 2)
        return math.sqrt(total)


class BM25Model(RetrievalModel):

    def __init__(self, data, documents):
        super().__init__(data, documents)
        self.k_1 = 1.2
        self.k_2 = 100
        self.b = 0.75
        self.avr_doc_length = self.get_average_document_length()

    # Gets the average length of a document
    def get_average_document_length(self):
        total_sum_of_terms = 0
        amnt = 0
        for doc in self.get_all_documents():
            for term in self.inv_index.keys():
                total_sum_of_terms += self.get_number_of_term_in_document(term, doc)
            amnt += 1
        return total_sum_of_terms / amnt

    # Gets the document's length AKA the total number of word occurrences
    def get_doc_length(self, doc):

        doc_length = 0
        for term in self.inv_index.keys():
            doc_length += self.get_number_of_term_in_document(term, doc)

        return doc_length

    # Calculates K for BM25
    def calculate_K(self, doc):
        doc_length = self.get_doc_length(doc)
        return self.k_1*((1-self.b) + (self.b * (doc_length/self.avr_doc_length)))

    # calculates the value for a single query word
    def calculate_query_term_value(self, term, doc, query_words):
        # Query word frequency
        qf_i = 0
        for word in query_words:
            if word == term:
                qf_i += 1

        # Calculate variables for equation
        K = self.calculate_K(doc)
        n_i = self.get_number_of_document_with_term(term)
        f_i = self.get_number_of_term_in_document(term, doc)
        N = self.get_number_of_documents()

        part_1 = math.log10(N / n_i)
        part_2 = ((self.k_1 + 1) * f_i)/(K + f_i)
        part_3 = ((self.k_2 + 1)*qf_i)/(self.k_2 + qf_i)

        return part_1 * part_2 * part_3

    # Generates a rank for a single document
    def generate_rank(self, query_words, doc):
        rank_sum = 0
        for term in query_words:
            rank_sum += self.calculate_query_term_value(term, doc, query_words)
        return rank_sum
