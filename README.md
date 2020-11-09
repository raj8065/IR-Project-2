# IR-Project-2

## Basic Operation
The System is run by running the run_search_engine.py file (whether through an IDE or "python3 run_search_engine.py").

Then a command line prompt will ask you to input a query or type 'quit' to stop receiving input.

After an input is given the system will generate two html files in the ./res/results directory named <TF_IDF_ or BM25_><Query Inputted>.html.

## Runnables
The runnable python files contained within are:

run_search_engine.py -> Runs the search engine

index_files.py -> Generates the inverted index, needs only to be run once

html_parser.py -> Generates the doc lookup and documents in the collection, needs only to be run once

#### Other Files
posting.py -> A class for holding inverted index information

result_page_generator.py -> Creates the HTML pages

retreival_models.py -> Contains classes for retreival models that calculate rankings

tsv_reader.py -> Reads the inverted index and the document lookup from the files
