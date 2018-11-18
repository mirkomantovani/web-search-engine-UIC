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


# def get_text_selectolax(html):
#     tree = HTMLParser(html)
#
#     if tree.body is None:
#         return None
#
#     for tag in tree.css('script'):
#         tag.decompose()
#     for tag in tree.css('style'):
#         tag.decompose()
#
#     text = tree.body.text(separator='\n')
#     return text
#
# print(get_text_selectolax(response.read().decode("utf-8")))
FOLDER = 'uic'
HOMEPAGE = 'https://www.uic.edu/'
DOMAIN_NAME = get_domain_name(HOMEPAGE)
PAGE_RANK_MAX_ITER = 20


def preprocess_documents():
    global link_extractor
    web_graph = graph.OptimizedDirectedGraph()

    with open('code_from_url_dict.pickle', 'rb') as handle:
        code_from_url = pickle.load(handle)

    for filename in os.listdir(FOLDER + '/pages/'):
        with open(FOLDER + '/pages/' + filename) as f:
            doc_text = f.read()
        link_extractor = LinkExtractor(FOLDER, HOMEPAGE, DOMAIN_NAME)
        link_extractor.feed(doc_text)
        links = link_extractor.page_links()
        # print('document number '+filename)
        # print('total links: '+str(len(links)))
        count = 0
        web_graph.add_node(int(filename))
        for url in links:
            if url in code_from_url:
                count += 1
                web_graph.add_edge(int(filename), code_from_url[url])
        # print('links in graph '+str(count))
        # print(web_graph)
    return web_graph


web_g = preprocess_documents()
print(web_g)
p_ranker = page_rank.PageRank()
ranks = p_ranker.page_rank(web_g, PAGE_RANK_MAX_ITER)

print(ranks)

web_g.get_pointing_to()




