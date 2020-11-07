import glob
import csv
import os
import re
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import word_tokenize
import re


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


    return doc_lookup_table

def write_index_to_tsv(inverted_index):
  index_file = os.path.join(os.path.dirname(os.getcwd())+"\\res\\inverted_index.tsv")
  with open(index_file, 'w') as out_file:
      tsv_writer = csv.writer(out_file, delimiter='\t')
      #tsv_writer.writerow(['Keyword', 'Number of Postings', 'Document Ids', 'Frequency'])
      for key,value in sorted(inverted_index.items()):
          posting = [key]
          p_list = inverted_index[key].get_posting_list()         
          posting.append(inverted_index[key].get_n_postings())
          for key, value in p_list.items():
              # flatten posting dict into list
              posting.append(key)
              posting.append(value)
        
          tsv_writer.writerow(posting)

snowball_stemmer = SnowballStemmer("english")


def get_word_stem(word):
    # utility method to use nltk stemming to get word stem
    return snowball_stemmer.stem(word)


def trim_word(word):
    if re.match("[\w\d]+", word):

        new_word = re.sub('[^\w\d\-]+', '', word)
        new_word = re.sub(r'[â]*([\w\d\-]+)[â]*', r'\1', new_word)

        if re.match("[\w\d]+", new_word):
            # Generates the capture group(s)
            capture_groups = re.search(("[-]*([\w\d]+[\w\d\-]*[\w\d]+|[\w\d]+)[-]*"), new_word)
            if capture_groups is None:
                raise Exception("Word was trimmed and no capture groups were created. WORD: ", new_word)
            if capture_groups.lastindex > 1:
                raise Exception("There was more than 1 capture group for wa word. WORD: ", new_word)
            return capture_groups.group(1)
    return ""


# Splits text into parts then for each part it trims it, strips it, puts it in lowercase and stems it
def clean_input(text):
    clean_terms = []

    # Split the text at these characters ...
    text_parts = re.split(" |\n|\xa0", text)

    # Process each term
    for part in text_parts:
        term = trim_word(part)
        if term != "":
            word = term.lower()
            term = get_word_stem(word)

            clean_terms.append(term)

    return clean_terms

def preprocess_word(word):

	word = word.lower()
	word_alpha_num = re.sub('[^A-Za-z0-9]+', '', word)
	return word_alpha_num

def gen_index(folder_path):
    inverted_index = {}
    doc_lookup_table = get_doc_lookup_table("res/doc_lookup.tsv")  # TODO change to class member

    transcript_folder = os.path.dirname(os.getcwd()) + "\\" + folder_path + "\\"

    ctr = 0

    for doc_id in doc_lookup_table.keys():
        file_name = transcript_folder + doc_lookup_table.get(doc_id)["file_name"]
        with open(file_name, 'r') as episode_transcript:

            # Gets the whole episode text
            source_code = episode_transcript.read()
            # Separates and cleans the terms of the text
            clean_terms = clean_input(source_code)

            # Adds each clean term to the inverted index
            for term in clean_terms:
                if not inverted_index.get(term):
                    inverted_index[term] = posting()
                inverted_index[term].record_instance_of_word(doc_id)

    # for (key, value) in inverted_index.items(): # FOR TESTING PURPOSES
    # 	print(key, value)
    return inverted_index


inverted_index = gen_index("res/out")
# print(get_doc_lookup_table("res/doc_lookup.tsv"))
write_index_to_tsv(inverted_index)
