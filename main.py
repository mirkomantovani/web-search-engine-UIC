# Mirko Mantovani
from preprocess import CustomTokenizer
from statistics import TfidfRanker, add_page_rank_scores_and_reorder
import CustomGUI as gui
import pickle
import time
from pseudo_relevance_feedback import CustomPseudoRelevanceFeedback
import webbrowser

'''
This script is the main program of this project, by running it the user is displayed a GUI where he can choose some
settings and start running his queries and seeing the results
'''
N_PAGES = 10000
RESULTS_PER_PAGE = 10
MAX_RESULTS_TO_CONSIDER = 100

# Default values overridden on application start when the users sets his preferences
USE_PAGE_RANK = False
USE_PAGE_RANK_EARLY = False  # I decided not to let the user choose this mode
USE_PSEUDO_RELEVANCE_FEEDBACK = True


def load_files():
    """Loading all the necessary files to run the queries and return ranked urls"""

    global url_from_code, code_from_url, inverted_index, docs_length, page_ranks, docs_tokens

    with open('url_from_code_dict.pickle', 'rb') as handle:
        url_from_code = pickle.load(handle)
    with open('code_from_url_dict.pickle', 'rb') as handle:
        code_from_url = pickle.load(handle)
    with open('inverted_index_dict.pickle', 'rb') as handle:
        inverted_index = pickle.load(handle)
    with open('doc_lengths_dict.pickle', 'rb') as handle:
        docs_length = pickle.load(handle)
    with open('page_ranks_dict.pickle', 'rb') as handle:
        page_ranks = pickle.load(handle)
    with open('docs_tokens_dict.pickle', 'rb') as handle:
        docs_tokens = pickle.load(handle)


def new_query():
    query = gui.ask_query()
    if query is None:
        exit()
    # print(query)
    query_tokens = tokenizer.tokenize(query)
    # print(query_tokens)

    best_ranked = tf_idf_ranker.retrieve_most_relevant(query_tokens, USE_PAGE_RANK_EARLY)[:MAX_RESULTS_TO_CONSIDER]

    if USE_PSEUDO_RELEVANCE_FEEDBACK:
        handle_pseudo_relevance_query(query_tokens, best_ranked)
    else:
        handle_normal_query(query_tokens, best_ranked)


def handle_normal_query(query_tokens, best_ranked):
    if USE_PAGE_RANK:
        best_ranked = add_page_rank_scores_and_reorder(best_ranked, page_ranks)
    handle_show_query(best_ranked, query_tokens, RESULTS_PER_PAGE)


def handle_pseudo_relevance_query(query_tokens, best_ranked):
    pseudo_relevance_feedback = CustomPseudoRelevanceFeedback(inverted_index, best_ranked, docs_tokens)
    pseudo_relevance_feedback.run_pseudo_relevance()
    query_expansion_tokens = pseudo_relevance_feedback.get_query_expansion_tokens(query_tokens)

    best_ranked_expanded = tf_idf_ranker.retrieve_most_relevant_expanded(query_tokens,
                                                                         query_expansion_tokens)[:MAX_RESULTS_TO_CONSIDER]

    if USE_PAGE_RANK:
        best_ranked_expanded = add_page_rank_scores_and_reorder(best_ranked_expanded, page_ranks)
    handle_show_query_expanded(best_ranked_expanded, query_tokens, query_expansion_tokens, RESULTS_PER_PAGE)

    # print(query_expansion_tokens)


def open_website(url):
    webbrowser.open(url.split()[0], new=2, autoraise=True)


def handle_show_query(best_ranked, query_tokens, n):
    choice = gui.display_query_results(best_ranked[:n], url_from_code, query_tokens)

    if choice == 'Show more results':
        handle_show_query(best_ranked, query_tokens, n + RESULTS_PER_PAGE)
    else:
        if choice is None:
            main_menu()
        else:
            if choice == 'Auto expand query':
                handle_pseudo_relevance_query(query_tokens, best_ranked)
            else:
                open_website(choice)
                main_menu()


def handle_show_query_expanded(best_ranked, query_tokens, query_expansion_tokens, n):
    choice = gui.display_query_results_expanded(best_ranked[:n], url_from_code, query_tokens, query_expansion_tokens)

    if choice == 'Show more results':
        handle_show_query_expanded(best_ranked, query_tokens, query_expansion_tokens, n + RESULTS_PER_PAGE)
    else:
        if choice is None:
            main_menu()
        else:
            open_website(choice)
            main_menu()


def setup_preferences():
    global USE_PAGE_RANK, USE_PSEUDO_RELEVANCE_FEEDBACK
    choice = gui.ask_preference('use Page Rank')
    USE_PAGE_RANK = choice
    choice = gui.ask_preference('use Context Pseudo Relevance feedback')
    USE_PSEUDO_RELEVANCE_FEEDBACK = choice


def main_menu():
    choice = gui.display_main_menu(USE_PAGE_RANK, USE_PSEUDO_RELEVANCE_FEEDBACK)
    execute_function(choice)


def execute_function(main_menu_choice):
    switcher = {
        'Setup search options': on_start_menu,
        'New query': new_query,
        'Exit UIC web search engine': exit_program,
    }
    # Get the function from switcher dictionary
    func = switcher.get(main_menu_choice, lambda: "nothing")
    return func()


def exit_program():
    exit()


def on_start_menu():
    setup_preferences()
    main_menu()


def start_engine():
    global tokenizer, tf_idf_ranker

    load_files()
    tokenizer = CustomTokenizer(N_PAGES)
    tf_idf_ranker = TfidfRanker(inverted_index, N_PAGES, page_ranks, docs_length, True)

    on_start_menu()


start_engine()
# load_files()

# for i in range(4401, 4437):
#     url_from_code[i] = url_from_code[i+5600]
#
# new = {}
# for i in code_from_url:
#
#     if 10037 > code_from_url[i] > 10000:
#         new[code_from_url[i]-5600] = i
#         print(i)
#         print(code_from_url[i])
#         print(code_from_url[i]-5600)
#         print(new[code_from_url[i]-5600])
#     else:
#         new[i] = code_from_url[i]
#
# with open('code_from_url_dict.pickle', 'wb') as handle:
#     pickle.dump(new, handle, protocol=pickle.HIGHEST_PROTOCOL)
#
# with open('url_from_code_dict.pickle', 'wb') as handle:
#     pickle.dump(url_from_code, handle, protocol=pickle.HIGHEST_PROTOCOL)
