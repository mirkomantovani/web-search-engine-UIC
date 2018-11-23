import math
from collections import Counter
import operator


def rank_docs(similarities):
    return sorted(similarities.items(), key=operator.itemgetter(1), reverse=True)


class TfidfRanker:

    page_rank_multiplier = 20

    def __init__(self, inverted_index, n_pages, page_ranks, docs_length={}, inverted_already_tf_idf=False,
                 use_cosine_sim=True):
        self.inverted_index = inverted_index
        self.n_pages = n_pages
        self.page_ranks = page_ranks
        self.idf = self.compute_idf()
        self.use_cosine_sim = use_cosine_sim
        self.doc_length = docs_length
        if not inverted_already_tf_idf:
            self.compute_all_tf_idf()
        # for code in range(self.n_pages):
        #     self.doc_length[code] = self.compute_doc_length(code, docs_tokens[code])

    def tf_idf(self, word, doc):
        # putting tfidf into inverted index, i should do it before storing inverted index!
        self.inverted_index[word][doc] = self.inverted_index[word][doc] * self.idf[word]
        return self.inverted_index[word][doc]

    def compute_idf(self):
        df = {}
        idf = {}
        for key in self.inverted_index.keys():
            df[key] = len(self.inverted_index[key].keys())
            idf[key] = math.log(self.n_pages / df[key], 2)
        return idf

    def inner_product_similarities(self, query):
        # dictionary in which I'll sum up the similarities of each word of the query with each document in
        # which the word is present, key is the doc number,
        # value is the similarity between query and document
        similarity = {}
        for word in query:
            wq = self.idf.get(word, 0)
            if wq != 0:
                for doc in self.inverted_index[word].keys():
                    similarity[doc] = similarity.get(doc, 0) + self.tf_idf(word, doc) * wq
        return similarity

    def compute_lengths(self, docs_tokens):
        for code in range(self.n_pages):
            self.doc_length[code] = self.compute_doc_length(code, docs_tokens[code])
        return self.doc_length

    def compute_doc_length(self, code, tokens):
        words_accounted_for = []
        length = 0
        for token in tokens:
            if token not in words_accounted_for:
                length += self.tf_idf(token, code) ** 2
                words_accounted_for.append(token)
        return math.sqrt(length)

    def query_length(self, query):
        # IMPORTANT: in this HW no query has repeated words, so I can skip the term frequency calculation
        # for the query, and just use idfs quared
        length = 0
        cnt = Counter()
        for w in query:
            cnt[w] += 1
        for w in cnt.keys():
            length += (cnt[w]*self.idf.get(w, 0)) ** 2
        return math.sqrt(length)

    def cosine_similarities(self, query):
        similarity = self.inner_product_similarities(query)
        for doc in similarity.keys():
            similarity[doc] = similarity[doc] / self.doc_length[doc] / self.query_length(query)
        return similarity

    def cosine_page_rank(self, query_tokens):
        cosine_similarity = self.cosine_similarities(query_tokens)
        cosine_page_rank_sim = {key: cosine_similarity[key]+self.page_ranks[key]*TfidfRanker.page_rank_multiplier
                                for key in cosine_similarity}
        return cosine_page_rank_sim

    def retrieve_most_relevant(self, query_tokens, use_page_rank=False):
        if use_page_rank:
            return rank_docs(self.cosine_page_rank(query_tokens))
        else:
            return rank_docs(self.cosine_similarities(query_tokens))

    '''This method precomputes all tf idf and stores them in inverted index [word] [doc]'''
    def compute_all_tf_idf(self):
        for word in self.inverted_index:
            for doc_key in self.inverted_index[word]:
                self.inverted_index[word][doc_key] = self.tf_idf(word, doc_key)
