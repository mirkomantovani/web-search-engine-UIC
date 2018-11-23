def extract_highest_tfidf_words(doc_code, inverted_index, docs_tokens):
    ranked_tokens = []
    for token in docs_tokens[doc_code]:
        ranked_tokens = inverted_index[token][doc_code]

    # rank ranked_tokens
    # get top 20 for instance and return them
    return ranked_tokens[:20]


def get_context_words(docs_highest_tf_idf_words):
    unique_tokens = {}
    for doc_key in unique_tokens.keys():
        for token in docs_highest_tf_idf_words[doc_key]:
            if token in unique_tokens:
                unique_tokens[token] = unique_tokens[token]+docs_highest_tf_idf_words[doc_key][token]
# order them
#     probably i would wanna take into account also how many docs contributed to the final count but not too much
#     because the most frequent words will always be the same (student etc.)
    return unique_tokens
