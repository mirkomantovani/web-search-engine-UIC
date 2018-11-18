from multithreaded_crawling import start_crawling
import time
from urllib.request import urlopen

# start = time.time()
# start_crawling()
# end = time.time()
#
# print("dio cane finito al tempo: "+str(end-start))
#
# end = time.time()

response = urlopen('https://www.uic.edu/service/equipment-lending/classroom-equipment-lending')
print(response.getheader('Content-Type'))
print(response.read().decode("utf-8"))

# if 'text/html' in response.getheader('Content-Type'):
#     html_bytes = response.read()
#     html_string = html_bytes.decode("utf-8")
# link_extractor = LinkExtractor(Crawler.base_url, page_url, True, Crawler.domain_name)
# link_extractor.feed(html_string)
