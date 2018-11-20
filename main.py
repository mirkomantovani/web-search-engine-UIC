from preprocess import CustomTokenizer
import page_rank
from statistics import TfidfRanker
import CustomGUI as gui
import pickle

PAGE_RANK_MAX_ITER = 20
N_PAGES = 109

with open('url_from_code_dict.pickle', 'rb') as handle:
    code_from_url = pickle.load(handle)


tokenizer = CustomTokenizer(N_PAGES)
web_g = tokenizer.preprocess_documents()
# print(web_g)
p_ranker = page_rank.PageRank()
ranks = p_ranker.page_rank(web_g, PAGE_RANK_MAX_ITER)

# print(ranks)

inverted_index = tokenizer.get_inverted_index()


tf_idf_ranker = TfidfRanker(inverted_index, N_PAGES, tokenizer.get_docs_tokens())

query = gui.ask_query()

print(query)
print(tokenizer.tokenize(query))
choice = gui.display_query_results(tf_idf_ranker.retrieve_most_relevant(tokenizer.tokenize(query))[:10])
print(choice)
