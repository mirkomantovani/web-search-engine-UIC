from preprocess import CustomTokenizer
import page_rank
from statistics import TfidfRanker
import CustomGUI as gui

PAGE_RANK_MAX_ITER = 20
N_PAGES = 109


# tokenizer = CustomTokenizer(N_PAGES)
# web_g = tokenizer.preprocess_documents()
# # print(web_g)
# p_ranker = page_rank.PageRank()
# ranks = p_ranker.page_rank(web_g, PAGE_RANK_MAX_ITER)
#
# # print(ranks)
#
# inverted_index = tokenizer.get_inverted_index()
#
#
# tf_idf_ranker = TfidfRanker(inverted_index, N_PAGES, tokenizer.get_docs_tokens())

query = gui.ask_query()

print(query)
