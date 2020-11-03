import glob
import csv
import os
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import word_tokenize 

class posting():

    def __init__(self):
        self.posting_list = {}

    def record_instance_of_word(self, doc_id):
    	if not self.posting_list.get(doc_id):
    		self.posting_list[doc_id] = 1
    	else:
    		self.posting_list[doc_id] = self.posting_list[doc_id] + 1

    def __str__(self):
    	return "Posting(posting_list="+self.posting_list.__str__() + ")"



def get_doc_lookup_table(rel_path):
	doc_lookup_table = {}
	doc_lookup_file = os.path.join(os.path.dirname(os.getcwd())+"\\"+rel_path)
	with open(doc_lookup_file, 'r') as f:
	  	idx_data = csv.reader(f, delimiter="\t", quotechar='"')
	  	for row in idx_data:
	  		if row==[]:
	  			#weed out empty rows
	  			continue

	  		doc_lookup_table[int(row[0])] = {"heading_id":row[1], "file_name": row[2]}
	
	
	return doc_lookup_table


snowball_stemmer = SnowballStemmer("english")
def get_word_stem(word):
	#utility method to use nltk stemming to get word stem
	return snowball_stemmer.stem(word)



def gen_index(folder_path):

	inverted_index = {}
	doc_lookup_table = get_doc_lookup_table("res/doc_lookup.tsv") #TODO change to class member

	transcript_folder = os.path.dirname(os.getcwd())+"\\"+folder_path + "\\"

	ctr = 0

	for doc_id in doc_lookup_table.keys():
		file_name = transcript_folder + doc_lookup_table.get(doc_id)["file_name"]
		with open(file_name, 'r') as episode_transcript:
			source_code = episode_transcript.read()
			for word in source_code.split():
				# TODO remove punctuation in word
				word = word.lower()
				stem = get_word_stem(word)
				
				if not inverted_index.get(stem):
					inverted_index[stem] = posting()
				
				inverted_index[stem].record_instance_of_word(doc_id)
					
				
			
		ctr = ctr + 1
		if ctr == 1: # FOR TESTING PURPOSES 
			break
	
	# for (key, value) in inverted_index.items(): # FOR TESTING PURPOSES 
	# 	print(key, value)




			
		
		
			


gen_index("res/out")
#print(get_doc_lookup_table("res/doc_lookup.tsv"))
