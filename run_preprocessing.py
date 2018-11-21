from preprocess import CustomTokenizer
import page_rank
from statistics import TfidfRanker
# import CustomGUI as gui
import pickle
import time
'''
This script opens the locally downloaded pages from the crawler, preprocess them, builds inverted index and
runs page rank, computes docs lengths, it then stores inverted index, page rank and docs length with pickle
'''
PAGE_RANK_MAX_ITER = 100
N_PAGES = 10000

USE_PAGE_RANK = True

# with open('url_from_code_dict.pickle', 'rb') as handle:
#     url_from_code = pickle.load(handle)

start = time.time()

print('Preprocessing '+str(N_PAGES)+' pages')
tokenizer = CustomTokenizer(N_PAGES)
web_g = tokenizer.preprocess_documents()

prep = time.time()
print('Total preprocessing time:')
print(str(prep-start)+' seconds')

# print(web_g)
print('Running page rank')
p_ranker = page_rank.PageRank()
page_ranks = p_ranker.page_rank(web_g, PAGE_RANK_MAX_ITER)

pr = time.time()
print('Total page rank running time:')
print(str(pr-prep)+' seconds')

# print(page_ranks)
print('Building inverted index')
inverted_index = tokenizer.get_inverted_index()

inv = time.time()
print('Total inverted index building time:')
print(str(inv-pr)+' seconds')

print('Computing docs lengths')
tf_idf_ranker = TfidfRanker(inverted_index, N_PAGES, page_ranks)
docs_length = tf_idf_ranker.compute_lengths(tokenizer.get_docs_tokens())

print('Storing files')
# storing page ranks
with open('page_ranks_dict.pickle', 'wb') as handle:
    pickle.dump(page_ranks, handle, protocol=pickle.HIGHEST_PROTOCOL)

# storing inverted index
with open('inverted_index_dict.pickle', 'wb') as handle:
    pickle.dump(inverted_index, handle, protocol=pickle.HIGHEST_PROTOCOL)

# storing doc lengths
with open('doc_lengths_dict.pickle', 'wb') as handle:
    pickle.dump(docs_length, handle, protocol=pickle.HIGHEST_PROTOCOL)

end = time.time()

print('total time:')
print(str(end-start)+' seconds')

# print('finished')
# def new_query():
#     query = gui.ask_query()
#     if query is None:
#         exit()
#     print(query)
#     print(tokenizer.tokenize(query))
#     choice = gui.display_query_results(tf_idf_ranker.retrieve_most_relevant(tokenizer.tokenize(query), False)[:10],
#                                        url_from_code)
#     print(choice)
#
#
# while 1:
#     new_query()