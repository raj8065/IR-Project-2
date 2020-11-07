import csv
import os
from index_files import posting

class Tsv_Reader():
	def __init__(self, doc_lookup_rel_path, inverted_index_rel_path):
		self.doc_lookup_rel_path = doc_lookup_rel_path
		self.inverted_index_rel_path = inverted_index_rel_path

	def get_doc_lookup_table(self):
		doc_lookup_table = {}
		doc_lookup_file = os.path.join(os.path.dirname(os.getcwd())+"\\"+self.doc_lookup_rel_path)
		with open(doc_lookup_file, 'r') as f:
			idx_data = csv.reader(f, delimiter="\t", quotechar='"')
			for row in idx_data:
				if row==[]:
					#weed out empty rows
				    continue
				doc_lookup_table[int(row[0])] = {"heading_id":row[1], "file_name": row[2]}
		return doc_lookup_table


	def get_inv_idx(self):
		inverted_index = {}
		inv_idx_file = os.path.join(os.path.dirname(os.getcwd())+"\\"+self.inverted_index_rel_path)
		with open(inv_idx_file, 'r') as f:
			idx_data = csv.reader(f, delimiter="\t", quotechar='"')
			for row in idx_data:
				if row==[]:
					#weed out empty rows
				    continue
				p_list = posting()
				p_list.populate_posting_list_from_array("\t".join(row))
				inverted_index[row[0]] = p_list
		return inverted_index
			

#tsv_reader = Tsv_Reader("res/doc_lookup.tsv", "res/inverted_index.tsv")

#inverted_index = tsv_reader.get_inv_idx()
#write_index_to_tsv(inverted_index)
#print(tsv_reader.get_doc_lookup_table())