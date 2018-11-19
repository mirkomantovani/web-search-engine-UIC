import math
from collections import Counter


class TfidfRanker:
    def __init__(self, inverted_index, n_pages, docs_tokens, use_cosine_sim=True):
        self.inverted_index = inverted_index
        self.n_pages = n_pages
        self.idf = self.compute_idf()
        self.use_cosine_sim = use_cosine_sim
        self.doc_length = {}
        for code in range(self.n_pages):
            self.doc_length[code] = self.compute_doc_length(code, docs_tokens[code])

    def tf_idf(self, word, doc):
        return self.inverted_index[word][doc] * self.idf[word]

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


