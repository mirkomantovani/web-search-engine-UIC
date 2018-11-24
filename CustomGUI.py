# Mirko Mantovani
import easygui as eg


def ask_query():
    msg = "Enter your query"
    title = "Query"
    # field_names = ["Query"]
    # fieldValues = []  # we start with blanks for the values
    # fieldValues = eg.multenterbox(msg, title, field_names)
    response = eg.enterbox(msg, title)
    return response


def display_query_results(docs_list, url_from_code, query_tokens):
    # url_from_code = Crawler.get_url_from_code()
    msg = "Preprocessed query: "+str(query_tokens)+"\nThese are the results of your query, you can double click" \
                                                   " or select and press ok on a" \
                                                   " result to open the web page in a new tab of your default browser" \
                                                   " or you can choose to Show more results. Press cancel to go back" \
                                                   " to the main menu."
    title = "Query results"
    # print(url_from_code)
    url_list = [str(url_from_code[code[0]])+' '+str(code[1]) for code in docs_list]
    url_list.append("Show more results")
    url_list.append("Auto expand query")
    choice = eg.choicebox(msg, title, url_list)
    return choice


def display_query_results_expanded(docs_list, url_from_code, query_tokens, query_expansion_tokens):
    msg = "Preprocessed query: " + str(query_tokens) + "\nExpanded query tokens : " + str(query_expansion_tokens) +\
          "\nThese are the results of your query, you can double click" \
                                                   " or select and press ok on a" \
                                                   " result to open the web page in a new tab of your default browser" \
                                                   " or you can choose to Show more results. Press cancel to go back" \
                                                   " to the main menu."
    title = "Expanded query results"
    # print(url_from_code)
    url_list = [str(url_from_code[code[0]]) + ' ' + str(code[1]) for code in docs_list]
    url_list.append("Show more results")
    choice = eg.choicebox(msg, title, url_list)
    return choice


def display_main_menu(use_page_rank, use_pseudo_relevance_feedback):
    # image = "python_and_check_logo.gif"
    msg = "Settings \nUse page rank: " + str(use_page_rank) + "\nUse Context pseudo relevance feedback: "\
          + str(use_pseudo_relevance_feedback) + "\n\nChoose your action"
    title = "Main menu UIC web search engine"
    choices = ["Setup search options", "New query", "Exit UIC web search engine"]
    choice = eg.buttonbox(msg, title, choices=choices)
    return choice


def ask_preference(use_feature_text):
    msg = "Do you want to "+use_feature_text+" feature in your future searches?"
    title = "Setup Preference"
    choice = eg.ynbox(msg, title)
    return choice
