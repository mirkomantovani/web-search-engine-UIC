# Mirko Mantovani
from selectolax.parser import HTMLParser
import pickle
from link_extractor import LinkExtractor
from domain_utils import *
import graph
import re
import string
from nltk.stem import PorterStemmer


class CustomTokenizer:

    def __init__(self, n_pages=10000, path_stopwords='stopwords.txt'):
        self.path_stopwords = path_stopwords
        self.inverted_index = {}
        self.FOLDER = 'uic'
        self.n_pages = n_pages
        self.HOMEPAGE = 'https://www.uic.edu/'
        self.DOMAIN_NAME = get_domain_name(self.HOMEPAGE)
        self.stemmer = PorterStemmer()
        # needed to compute doc length faster
        self.docs_tokens = {}
        with open(self.path_stopwords, "r") as stop_file:
            self.stop_words = stop_file.readlines()
        self.stop_words = list(map(lambda x: x[:-1], self.stop_words))

    @staticmethod
    def get_text_selectolax(html):
        tree = HTMLParser(html)

        if tree.body is None:
            return None

        for tag in tree.css('script'):
            tag.decompose()
        for tag in tree.css('style'):
            tag.decompose()

        text = tree.body.text(separator=' ')
        return text

    def get_inverted_index(self):
        return self.inverted_index

    def get_docs_tokens(self):
        return self.docs_tokens

    def process_page(self, code, doc_text):
        doc_text = self.get_text_selectolax(doc_text)
        # print(code)
        if doc_text is None:
            # print(str(code)+' is none')
            doc_text = 'none'
        tokens = self.tokenize(doc_text)
        # print(list(tokens))
        self.docs_tokens[code] = tokens
        self.add_in_inverted_index(code, tokens)
        # exit()

    def add_in_inverted_index(self, code, tokens):
        for token in tokens:
            self.inverted_index.setdefault(token, {})[code] = self.inverted_index.setdefault(token, {}).get(code, 0) + 1
        # print(self.inverted_index)

    def tokenize(self, doc_text):
        tokens = doc_text.split()
        tokens = [''.join(c for c in t if c not in string.punctuation) for t in tokens]
        tokens = [t.lower() for t in tokens]
        tokens = map(replace_digits, tokens)
        # stemming needed before stop word elimination because some stop-words could be stemmed
        # and become non-stop-words, i.e. "has" -> "ha", "anyone" -> "anyon"
        # print(list(tokens))
        tokens = map(self.stemmer.stem, tokens)
        tokens = [t for t in tokens if not lesseq_two_letters(t)]
        # stop words elimination
        # print(len(list(tokens)))
        # print(self.stop_words)
        tokens = [t for t in tokens if t not in self.stop_words]
        # print(len(tokens))
        tokens = [t for t in tokens if t]
        return tokens

    def preprocess_documents(self):
        global link_extractor
        web_graph = graph.OptimizedDirectedGraph()

        with open('code_from_url_dict.pickle', 'rb') as handle:
            code_from_url = pickle.load(handle)

        # for filename in os.listdir(self.FOLDER + '/pages/'):
        for filename in range(self.n_pages):
            with open(self.FOLDER + '/pages/' + str(filename)) as f:
                doc_text = f.read()

            if doc_text is None:
                print('empty doc')
                print(filename)
                continue

            self.process_page(int(filename), doc_text)

            link_extractor = LinkExtractor(self.FOLDER, self.HOMEPAGE, self.DOMAIN_NAME)
            link_extractor.feed(doc_text)
            links = link_extractor.page_links()
            # print('document number '+filename)
            # print('total links: '+str(len(links)))
            count = 0
            web_graph.add_node(int(filename))
            for url in links:
                if url in code_from_url:
                    # if code_from_url[url] == 6:
                    #     print(url)
                    #     exit()
                    count += 1
                    web_graph.add_edge(int(filename), code_from_url[url])
            # print('node '+filename+str(web_graph.get_pointing_to(int(filename))))
        return web_graph


# removing digits and returning the word
def replace_digits(st):
    return re.sub('\d', '', st)


# returns true if the word has less or equal 2 letters
def lesseq_two_letters(word):
    return len(word) <= 2






