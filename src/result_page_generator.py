import html
import os
import re

from src.tsv_reader import Tsv_Reader


def generate_html_top(file, query):
    top_top = "<div><a>&lt;Search Engine Name Here&gt;</a><div\"><form><input type=\"text\" value=\""
    bottom_top = "\" /><input type=\"submit\" value=\"Submit\" /></form></div></div>"
    file.write(top_top)
    file.write(html.escape(query))
    file.write(bottom_top)


def generate_html_bottom(file):
    file.write("")


def generate_html_result(file, doc):
    title = html.escape(doc['file_name'])
    path = os.path.join("\"..\\out\\" + title + "\"")

    # Description under the title
    description = html.escape("INSERT DESCRIPTION HERE")
    # Bolds targeted query words
    description = re.sub(r'(query_word)', r'<strong>\1</strong>', description)

    file.write("<h2><a href=" + path + ">")
    file.write(title)
    file.write("</a></h2>")
    file.write("<div><a href=" + path + "><span>" + path + "</span></a></div>")
    file.write("<div>" + description + "</div>")


def generate_new_result_file_name(query):
    name = "".join(x for x in query if x.isalnum() or x is "_" or x is "-")
    return os.path.join(os.path.dirname(os.getcwd())+"\\res\\results\\" + name + ".html")


def generate_html_page(query, top_rankings):
    tsv_reader = Tsv_Reader("res\\doc_lookup.tsv", "res\\inverted_index.tsv")
    doc_lookup = tsv_reader.get_doc_lookup_table()

    f = open(generate_new_result_file_name(query), 'w')

    generate_html_top(f, query)

    for doc in top_rankings:
        generate_html_result(f, doc_lookup[doc])

    generate_html_bottom(f)
    f.close()

# Test case
generate_html_page("INSERT_QUERY_HERE",[0,1])