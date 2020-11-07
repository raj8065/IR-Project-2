import glob
import csv
import os
import re
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import word_tokenize
from tsv_reader import Tsv_Reader
from posting import posting


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
    # The characters we don't want in the beginning/end of the word
    removal_characters = "\]\[:,;\'\"”“\s?!.�\-"
    # The characters we want to allow as the characters of the word
    tar_char = "[\wâ€Ã©]"

    # Checks if the inputted word has any desired characters
    target_characters = re.search(tar_char, word)
    if target_characters is None:
        return ""

    # Generates the possible words that we want to keep
    target_word = "(" + tar_char + "+[\'-]+" + tar_char + "*[\'-]*" + tar_char + "+|" + tar_char + "+)"
    # Generates the regex to parse the input
    reg_ex = "^[" + removal_characters + "]*" + target_word + "[" + removal_characters + "]*$"

    # Generates the capture group(s)
    capture_groups = re.search(reg_ex, word)
    if capture_groups is None:
        raise Exception("Word was trimmed and no capture groups were created. WORD: ", word)
    if capture_groups.lastindex > 1:
        raise Exception("There was more than 1 capture group for wa word. WORD: ", word)
    return capture_groups.group(1)


# Splits text into parts then for each part it trims it, strips it, puts it in lowercase and stems it
def clean_input(text):
    clean_terms = []

    # Split the text at these characters ...
    text_parts = re.split(" |”|\n|\[|\[", text)

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
    tsv_reader = Tsv_Reader("res\\doc_lookup.tsv","")
    doc_lookup_table = tsv_reader.get_doc_lookup_table()  # TODO change to class member

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

        ctr = ctr + 1
        # if ctr == 1:  # FOR TESTING PURPOSES
        #     break

    # for (key, value) in inverted_index.items(): # FOR TESTING PURPOSES
    # 	print(key, value)
    return inverted_index


inverted_index = gen_index("res/out")
# print(get_doc_lookup_table("res/doc_lookup.tsv"))
write_index_to_tsv(inverted_index)
