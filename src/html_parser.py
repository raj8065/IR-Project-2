from bs4 import BeautifulSoup
import requests
import re
import csv

class html_parser():

    def __init__(self, transcript_doc, doc_lookup_table, soup):
        self.transcript_doc = transcript_doc
        self.doc_lookup_table = doc_lookup_table
        self.soup = soup

    def get_document_soup(self):
        with open(self.transcript_doc) as fp:
            self.soup = BeautifulSoup(fp, 'html5lib')

    def populate_doc_lookup_table(self):
        #with open("../res/first_five.html") as fp:
        with open(self.transcript_doc) as fp:
            
            data = self.soup.find('div',attrs={'id':"transcripts-toc"})
            docId = 0
            transcript_links = data.findAll('a')
            for a in transcript_links:   
                heading_id = a['href'].replace("#","")
                pattern = "[" + "<>:\"/\\|?*" + "]"
                file_name = re.sub(pattern, "", a.contents[0])    
                self.doc_lookup_table[docId] = {'heading_id': heading_id, 'file_name': file_name}
                docId = docId + 1
                # if docId == 30:
                #     break

    def write_transcripts_to_files(self):
        for docId,value in self.doc_lookup_table.items():
                
            data = self.soup.find('h2',attrs={'id':value.get('heading_id')})
            currNode = data
            currHtml = ""
            for _ in data.next_siblings:
                currNode = currNode.nextSibling            

                if currNode == None or currNode.name==None:
                    continue
                if currNode.name == "h2":
                    break
                else:
                    currHtml = currHtml + str(currNode.text)


            f = open("../out/"+value.get('file_name'), "w")
            f.write(currHtml)
            f.close()           


    def write_doc_table_to_tsv(self):
        with open('../res/doc_lookup.tsv', 'w') as out_file:
            tsv_writer = csv.writer(out_file, delimiter='\t')
            for key,value in self.doc_lookup_table.items():
                tsv_writer.writerow([key,
                    self.doc_lookup_table[key]["heading_id"],
                    self.doc_lookup_table[key]["file_name"]])


    def main(self):
        self.get_document_soup()
        self.populate_doc_lookup_table()
        self.write_transcripts_to_files()
        self.write_doc_table_to_tsv()


if __name__ == '__main__':
    mlp_transcript_parser = html_parser("../res/all_mlp_transcripts.html", {}, None)
    mlp_transcript_parser.main()

