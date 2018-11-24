# Mirko Mantovani

import operator

NUMBER_DOCS_EXPANSION = 30
NUMBER_TOP_TOKENS = 10
NUMBER_EXPANSION_TOKENS = 10


def convert_list_tuples_to_dict(list_tuples):
    new_dict = {}
    for elem in list_tuples:
        new_dict[elem[0]] = elem[1]
    return new_dict


class CustomPseudoRelevanceFeedback:

    def __init__(self, inverted_index, top_docs, docs_tokens):
        self.top_words_number = NUMBER_TOP_TOKENS
        self.expansion_tokens_number = NUMBER_EXPANSION_TOKENS
        self.top_docs = top_docs[:NUMBER_DOCS_EXPANSION]
        '''top_docs_list are the list of tuples (doc_code, sim) retrieved by the query'''
        self.inverted_index = inverted_index
        '''Inverted index is already with tf idf inside'''
        self.docs_tokens = docs_tokens
        '''the documents tokens (dict) to faster extract top tfidf words'''
        self.docs_highest_tfidf = {}
        self.context_words = {}

    '''Runs the custom pseudo relevance feedback algorithm and returns an ordered list of tuples (token, 
    cumulativeTfidf) '''
    def run_pseudo_relevance(self):
        for doc_code in self.top_docs:
            # doc_code[0] is the doc code
            self.docs_highest_tfidf[doc_code[0]] = self.extract_highest_tfidf_words(doc_code[0])
        return self.get_context_words()

    '''Extracts the words with highest tfidf in a doc with code doc_code and returns a dict of the
            self.top_words_number words '''
    def extract_highest_tfidf_words(self, doc_code):
        ranked_tokens = {}
        for token in self.docs_tokens[doc_code]:
            ranked_tokens[token] = self.inverted_index[token][doc_code]

        ranked_tokens = sorted(ranked_tokens.items(), key=operator.itemgetter(1), reverse=True)
        # get top 20 for instance and return them
        return convert_list_tuples_to_dict(ranked_tokens[:self.top_words_number])
        # return ranked_tokens[:20]

    def get_query_expansion_tokens(self, initial_query_tokens, expansion_length=-1):
        if expansion_length <= 0:
            expansion_length = self.expansion_tokens_number
        expansion_tokens = [token[0] for token in self.context_words[:expansion_length]]
        for query_token in initial_query_tokens:
            if query_token in expansion_tokens:
                expansion_tokens.remove(query_token)
        return expansion_tokens

    def get_context_words(self):
        unique_tokens = {}
        for doc_key in self.docs_highest_tfidf.keys():
            for token in self.docs_highest_tfidf[doc_key]:
                if token in unique_tokens:
                    unique_tokens[token] = unique_tokens[token] + self.docs_highest_tfidf[doc_key][token]
                else:
                    unique_tokens[token] = self.docs_highest_tfidf[doc_key][token]

        # ordering unique tokens based on cumulative tfidfs
        unique_tokens = sorted(unique_tokens.items(), key=operator.itemgetter(1), reverse=True)
        # probably i would wanna take into account also how many docs contributed to the final count but not too much
        #  because the most frequent words will always be the same (student etc.)
        self.context_words = unique_tokens
        return unique_tokens




