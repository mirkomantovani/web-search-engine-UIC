# Mirko Mantovani
from preprocess import CustomTokenizer
import page_rank
from statistics import TfidfRanker
import pickle
import time

'''
This script opens the locally downloaded pages from the crawler, preprocess them, builds inverted index and
runs page rank, computes docs lengths, it then stores inverted index, page rank and docs length with pickle
'''
PAGE_RANK_MAX_ITER = 100
N_PAGES = 10000

start = time.time()

print('Preprocessing '+str(N_PAGES)+' pages')
tokenizer = CustomTokenizer(N_PAGES)
web_g = tokenizer.preprocess_documents()
docs_tokens = tokenizer.get_docs_tokens()

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

inverted_index = tokenizer.get_inverted_index()


print('Computing docs lengths')
tf_idf_ranker = TfidfRanker(inverted_index, N_PAGES, page_ranks)
docs_length = tf_idf_ranker.compute_lengths(tokenizer.get_docs_tokens())
# Taking the new inverted index with tf idf inside
inverted_index = tf_idf_ranker.inverted_index

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

# storing docs tokens for faster pseudo-relevance feedback
with open('docs_tokens_dict.pickle', 'wb') as handle:
    pickle.dump(docs_tokens, handle, protocol=pickle.HIGHEST_PROTOCOL)

end = time.time()

print('total time:')
print(str(end-start)+' seconds')

