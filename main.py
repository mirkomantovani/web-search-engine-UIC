from preprocess import CustomTokenizer
import page_rank
from statistics import TfidfRanker
import CustomGUI as gui
import pickle

PAGE_RANK_MAX_ITER = 20
N_PAGES = 1000

USE_PAGE_RANK = True

with open('url_from_code_dict.pickle', 'rb') as handle:
    url_from_code = pickle.load(handle)

print('Preprocessing '+str(N_PAGES)+' pages')
tokenizer = CustomTokenizer(N_PAGES)
web_g = tokenizer.preprocess_documents()
# print(web_g)
print('Running page rank')
p_ranker = page_rank.PageRank()
page_ranks = p_ranker.page_rank(web_g, PAGE_RANK_MAX_ITER)

print(page_ranks)
print('Building inverted index')
inverted_index = tokenizer.get_inverted_index()

print('Computing docs lengths')
tf_idf_ranker = TfidfRanker(inverted_index, N_PAGES, page_ranks, tokenizer.get_docs_tokens())


def new_query():
    query = gui.ask_query()
    if query is None:
        exit()
    print(query)
    print(tokenizer.tokenize(query))
    choice = gui.display_query_results(tf_idf_ranker.retrieve_most_relevant(tokenizer.tokenize(query))[:10],
                                       url_from_code)
    print(choice)


while 1:
    new_query()
