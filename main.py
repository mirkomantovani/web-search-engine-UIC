from multithreaded_crawling import start_crawling
from selectolax.parser import HTMLParser
import time
from urllib.request import urlopen
import pickle
from link_extractor import LinkExtractor
from domain_utils import *

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

with open('code_from_url_dict.pickle', 'rb') as handle:
    code_from_url = pickle.load(handle)

with open(FOLDER+'/pages/'+'0') as page:
    first = page.read()

link_extractor = LinkExtractor(FOLDER, HOMEPAGE, DOMAIN_NAME)
link_extractor.feed(first)
links = link_extractor.page_links()
count = 0
print(len(links))
print()
for url in links:
    if url in code_from_url:
        count +=1
        print(code_from_url[url])
    else:
        print(url)
print()
print(count)

    # for filename in os.listdir(DOCS_PATH):
    #     if not filename.startswith('.') and filename in os.listdir(GOLD_PATH):
    #         doc_text = open(DOCS_PATH + filename).read()


