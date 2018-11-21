import easygui as eg
from crawler import Crawler


def ask_query():
    msg = "Enter your query"
    title = "Query"
    # field_names = ["Query"]
    # fieldValues = []  # we start with blanks for the values
    # fieldValues = eg.multenterbox(msg, title, field_names)
    response = eg.enterbox(msg, title)
    return response


def display_query_results(docs_list, url_from_code):
    # url_from_code = Crawler.get_url_from_code()
    msg = "These are the results of your query:"
    title = "Query results"
    # print(url_from_code)
    url_list = [str(url_from_code[code[0]])+' '+str(code[1]) for code in docs_list]
    choice = eg.choicebox(msg, title, url_list)
    return choice
