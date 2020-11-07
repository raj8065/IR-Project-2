class posting():

    def __init__(self):      
        self.posting_list = {}

    def populate_posting_list_from_array(self, posting_list_str):
        posting_list = posting_list_str.split("\t")

        for idx in range(2,len(posting_list)-1, 2):
            # elements 0 and 1 are the word itself and n_postings
            doc_id = int(posting_list[idx].replace("\'", ""))
            doc_freq = int(posting_list[idx+1].replace("\'", ""))
            self.posting_list[doc_id] = doc_freq
                  

    def get_posting_list(self):
        return self.posting_list

    def get_n_postings(self):
        return len(self.posting_list)

    def record_instance_of_word(self, doc_id):
        if not self.posting_list.get(doc_id):
            self.posting_list[doc_id] = 1
        else:
            self.posting_list[doc_id] = self.posting_list[doc_id] + 1

    def __str__(self):
        return "Posting(posting_list="+self.posting_list.__str__() + ")"