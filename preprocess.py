from multithreaded_crawling import start_crawling
from selectolax.parser import HTMLParser
import time
from urllib.request import urlopen
import pickle
from link_extractor import LinkExtractor
from domain_utils import *
import os
import graph
import page_rank
import re
import string
from nltk.stem import PorterStemmer

# start = time.time()
# start_crawling()
# end = time.time()
#
# print("dio cane finito al tempo: "+str(end-start))
#
# end = time.time()
# http://dentistry.uic.edu/sites/default/files/IMCE/research/ResearchDay/CRDayAwards-2013.pdf
# response = urlopen('https://www.cs.uic.edu/undergraduate-admissions/#1476482486945-df37d302-14b5')
# response = urlopen('http://dentistry.uic.edu/sites/default/files/IMCE/research/ResearchDay/CRDayAwards-2013.pdf')
# print(response.getheader('Content-Type'))
# print(response.read().decode("utf-8"))

# if 'text/html' in response.getheader('Content-Type'):
#     html_bytes = response.read()
#     html_string = html_bytes.decode("utf-8")
# link_extractor = LinkExtractor(Crawler.base_url, page_url, True, Crawler.domain_name)
# link_extractor.feed(html_string)

PAGE_RANK_MAX_ITER = 20


class CustomTokenizer:

    def __init__(self, path_stopwords='stopwords.txt'):
        self.path_stopwords = path_stopwords
        self.inverted_index = {}
        self.FOLDER = 'uic'
        self.HOMEPAGE = 'https://www.uic.edu/'
        self.DOMAIN_NAME = get_domain_name(self.HOMEPAGE)
        self.stemmer = PorterStemmer()
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

    def process_page(self, code, doc_text):
        doc_text = self.get_text_selectolax(doc_text)
        tokens = self.tokenize(doc_text)
        # print(list(tokens))
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

        for filename in os.listdir(self.FOLDER + '/pages/'):
            with open(self.FOLDER + '/pages/' + filename) as f:
                doc_text = f.read()

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


tokenizer = CustomTokenizer()
web_g = tokenizer.preprocess_documents()
print(web_g)
p_ranker = page_rank.PageRank()
ranks = p_ranker.page_rank(web_g, PAGE_RANK_MAX_ITER)

print(ranks)

print(tokenizer.get_inverted_index())

# import operator
# ranks = sorted(ranks.items(), key=operator.itemgetter(1))
# print(ranks)





