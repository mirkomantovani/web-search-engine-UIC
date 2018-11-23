import operator


def convert_list_tuples_to_dict(list_tuples):
    new_dict = {}
    for elem in list_tuples:
        new_dict[elem[0]] = elem[1]
    return new_dict


class CustomPseudoRelevanceFeedback:

    def __init__(self, inverted_index, top_docs, docs_tokens):
        self.top_words_number = 20
        self.top_docs = top_docs
        '''top_docs_list are the list of tuples (doc_code, sim) retrieved by the query'''
        self.inverted_index = inverted_index
        '''Inverted index is already with tf idf inside'''
        self.docs_tokens = docs_tokens
        '''the documents tokens (dict) to faster extract top tfidf words'''
        self.docs_highest_tfidf = {}

    def run_pseudo_relevance(self):
        for doc_code in self.top_docs:
            # doc_code[0] is the doc code
            self.docs_highest_tfidf[doc_code[0]] = self.extract_highest_tfidf_words(doc_code[0])
        self.get_context_words()

    '''Extracts the words with highest tfidf in a doc with code doc_code and returns a dict of the
            self.top_words_number words '''
    def extract_highest_tfidf_words(self, doc_code):
        ranked_tokens = {}
        for token in self.docs_tokens[doc_code]:
            ranked_tokens[token] = self.inverted_index[token][doc_code]

        ranked_tokens = sorted(ranked_tokens.items(), key=operator.itemgetter(1))
        # get top 20 for instance and return them
        return convert_list_tuples_to_dict(ranked_tokens[:self.top_words_number])
        # return ranked_tokens[:20]

    def get_context_words(self):
        unique_tokens = {}
        for doc_key in self.docs_highest_tfidf.keys():
            for token in self.docs_highest_tfidf[doc_key]:
                if token in unique_tokens:
                    unique_tokens[token] = unique_tokens[token] + self.docs_highest_tfidf[doc_key][token]
                else:
                    unique_tokens[token] = self.docs_highest_tfidf[doc_key][token]
        # order them
        #     probably i would wanna take into account also how many docs contributed to the final count but not too much
        #     because the most frequent words will always be the same (student etc.)
        return unique_tokens




