import html
import os
import re

import index_files
from tsv_reader import Tsv_Reader


def generate_hit_summary(query, doc):
    clean_query = index_files.clean_input(query)

    doc_file_name = doc['file_name']
    f = open(os.path.join(os.path.dirname(os.getcwd())+"\\res\\out\\" + doc_file_name), 'r')

    # Raw file input
    first_line = None
    second_line = None
    third_line = None

    # Cleaned file input
    first_line_clean = None
    second_line_clean = None
    third_line_clean = None

    # Best quote match
    top_score = None
    top_score_line = None

    for line in f:
        if first_line is not None and second_line is not None:
            # Find the intersection of the query and the lines
            quote = first_line_clean + second_line_clean + third_line_clean
            score = len([x for x in quote if x in clean_query])

            # If there is no top score, or if this one is better make it the top
            if top_score is None or score > top_score:
                top_score = score
                top_score_line = "<p>" + first_line + "<p>" + second_line + "<p>" + third_line + ""
        # Move the raw lines up
        first_line = second_line
        second_line = third_line
        third_line = line

        # Move the clean lines up
        first_line_clean = second_line_clean
        second_line_clean = third_line_clean
        third_line_clean = index_files.clean_input(third_line)

    return top_score_line


def generate_html_top(file, query):
    top_top = "<body style=\"background-color:#D0D0D0;\"><div><h1>My Little Pony Script Search Engine</h1><div\"><form><input type=\"text\" size=\"100\" value=\""
    bottom_top = "\" /><input type=\"submit\" value=\"Submit\" /></form></div></div>"
    file.write(top_top)
    file.write(html.escape(query))
    file.write(bottom_top)


def generate_html_bottom(file):
    file.write("</body>")


def generate_html_result(file, query, doc):
    title = html.escape(doc['file_name'])
    path = os.path.join("\"..\\out\\" + title + "\"")

    # Description under the title
    description = generate_hit_summary(query, doc)

    # Bolds targeted query words
    words = set([index_files.trim_word(x) for x in re.split(" |\n|\xa0", query)])
    if '' in words:
        words.remove('')
    description = re.sub('\\b(' + "|".join(words) + ')\\b', r'<strong>\1</strong>', description, flags=re.IGNORECASE)

    file.write("<h2><a href=" + path + ">")
    file.write(title)
    file.write("</a></h2>")
    file.write("<div><a href=" + path + "><span>" + path + "</span></a></div>")
    file.write("<div>" + description + "</div>")


def generate_new_result_file_name(file_name_prefix, query):
    name = "".join(x for x in file_name_prefix if x.isalnum() or x == "_" or x == "-") \
           + "".join(x for x in query if x.isalnum() or x == "_" or x == "-")
    return os.path.join(os.path.dirname(os.getcwd())+"\\res\\results\\" + name + ".html")


def generate_html_page(file_name_prefix, query, top_rankings):
    tsv_reader = Tsv_Reader("res\\doc_lookup.tsv", "res\\inverted_index.tsv")
    doc_lookup = tsv_reader.get_doc_lookup_table()

    f = open(generate_new_result_file_name(file_name_prefix, query), 'w')

    generate_html_top(f, query)

    for doc in top_rankings:
        generate_html_result(f, query, doc_lookup[doc])

    generate_html_bottom(f)
    f.close()

if __name__ == "__main__":
    # Test case
    generate_html_page("BM25", "We should do the annual Big-Sister-Little-Sister camping trip", [2, 0, 1, 8, 3, 6, 24, 10])