import math


class RetrievalModel:

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

    # TODO change depending on datamodel
    # Returns the id of the document
    def get_document_id(self, doc):
        return doc[0]

    # Returns the number of documents in which the term appears AKA n_k
    def get_number_of_document_with_term(self, term):
        if term in self.document_with_term_occurrences:
            return self.document_with_term_occurrences[term]

        sum = 0
        for doc in self.get_documents_for_term(term):
            sum = sum + 1
        self.document_with_term_occurrences[term] = sum

        return sum

    # Generates the ranks for all the documents AKA the main workhorse of the class
    def generate_ranks(self, query_words):
        ranks = dict()
        for doc in self.get_all_documents():
            ranks[self.get_document_id(doc)] = self.generate_rank(query_words, doc)
        return ranks

    # Generates a rank for a single document
    def generate_rank(self, query_words, doc):
        raise Exception('RetreivalModel superclass used to create a rank.')


class TfIdfModel(RetrievalModel):

    # Generates a rank for a single document
    def generate_rank(self, query_words, doc):
        denominator = self.generate_tf_idf_term_rank_denominator(self, doc)
        rank_sum = 0
        for word in query_words:
            rank_sum = rank_sum + self.generate_tf_idf_term_rank(word, doc, denominator)
        return rank_sum

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


def BM25Model(RetrievalModel):

    def __init__(self, doc_num, data, documents, k_1, k_2, b, avr_doc_length):
        super.__init__(self, doc_num, data, documents)
        self.k_1 = k_1
        self.k_2 = k_2
        self.b = b
        self.avr_doc_length = avr_doc_length

    # TODO Get the document's length
    def get_doc_length(self, doc):
        return 0

    # Calculates K for BM25
    def calculate_K(self, doc):
        doc_length = get_doc_length(doc)
        return self.k_1*((1-self.b) + (self.b * (doc_length/self.avr_doc_length)))

    def get_query_relevance(self):
        return 0

    def get_number_of_relevant(self):
        return 0

    # calculates the value for a single query word
    def calculate_query_term_value(self, term, doc, query_words):
        # Query word frequency
        qf_i = 0
        for word in query_words:
            if word == term:
                qf_i += 1

        # Calculate variables for equation
        K = self.calculate_K(doc)
        r_i = self.get_query_relevance()
        R = self.get_number_of_relevant()
        n_i = self.get_number_of_document_with_term(term)
        f_i = self.get_number_of_term_in_document(term, doc)
        N = self.get_number_of_documents()

        part_1_num = (r_i + 0.5)/(R - r_i + 0.5)
        part_1_denom = (n_i - r_i + 0.5)/(N - n_i - R + r_i + 0.5)
        part_1 = math.log10(part_1_num/part_1_denom)
        part_2 = ((self.k_1 + 1) * f_i)/(K + f_i)
        part_3 = ((self.k_2 + 1)*qf_i)/(self.k_2 + qf_i)

        return part_1 * part_2 * part_3

    # Generates a rank for a single document
    def generate_rank(self, query_words, doc):
        rank_sum = 0
        for term in query_words:
            rank_sum = calculate_query_term_value(self, term, doc)
        return rank_sum
