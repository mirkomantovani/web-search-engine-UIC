# Mirko Mantovani
from urllib.request import urlopen
from link_extractor import LinkExtractor
from crawling_utils import *
import pickle


class Crawler:
    folder = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    pages_folder = ''
    save_html_pages = True
    queue = set()
    crawled = set()
    code_from_url = {}
    url_from_code = {}
    count_code = 0

    def __init__(self, folder, base_url, domain_name):
        # print(Crawler.crawled)
        # with open('code_from_url_dict.pickle', 'rb') as handle:
        #     Crawler.code_from_url = pickle.load(handle)
        # with open('url_from_code_dict.pickle', 'rb') as handle:
        #     Crawler.url_from_code = pickle.load(handle)
        Crawler.folder = folder
        Crawler.base_url = base_url
        Crawler.domain_name = domain_name
        Crawler.queue_file = Crawler.folder + '/queue.txt'
        Crawler.crawled_file = Crawler.folder + '/crawled.txt'
        Crawler.pages_folder = Crawler.folder + '/pages/'
        self.boot()
        self.crawl_page('First crawler', Crawler.base_url)

    # Creates directory and files for project on first run and starts the spider
    @staticmethod
    def boot():
        # Crawler.count_code = 0
        create_domain_directory(Crawler.folder)
        create_domain_directory(Crawler.pages_folder)
        create_data_files(Crawler.folder, Crawler.base_url)
        Crawler.queue = get_set_from_file(Crawler.queue_file)
        Crawler.crawled = get_set_from_file(Crawler.crawled_file)

    # Updates user display, fills queue and updates files
    @staticmethod
    def crawl_page(thread_name, page_url):
        # print(page_url)
        # print(Crawler.crawled)
        if page_url not in Crawler.crawled:
            print(thread_name + ' now crawling ' + page_url)
            print('Queue ' + str(len(Crawler.queue)) + ' | Crawled  ' + str(len(Crawler.crawled)))
            Crawler.add_links_to_queue(Crawler.gather_links_save_page(page_url))
            Crawler.queue.remove(page_url)
            Crawler.crawled.add(page_url)
            Crawler.update_files()

    # Converts raw response data into readable information and checks for proper html formatting
    @staticmethod
    def gather_links_save_page(page_url):
        html_string = ''
        try:
            response = urlopen(page_url, timeout=10)
            if 'text/html' in response.getheader('Content-Type'):
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
                if Crawler.save_html_pages:
                    # By running concurrent threads this creates multiple equal codes
                    code = Crawler.count_code
                    Crawler.count_code += 1
                    write_file(Crawler.pages_folder+str(code), html_string)
                    Crawler.code_from_url[page_url] = code
                    Crawler.url_from_code[code] = page_url
                    if code % 100 == 0:
                        print('storing with pickle: code_from_url and url_from_code')
                        with open('code_from_url_dict.pickle', 'wb') as handle:
                            pickle.dump(Crawler.code_from_url, handle, protocol=pickle.HIGHEST_PROTOCOL)
                        with open('url_from_code_dict.pickle', 'wb') as handle:
                            pickle.dump(Crawler.url_from_code, handle, protocol=pickle.HIGHEST_PROTOCOL)
                            # with open('filename.pickle', 'rb') as handle:
                            #     b = pickle.load(handle)
            link_extractor = LinkExtractor(Crawler.base_url, page_url, True, Crawler.domain_name)
            link_extractor.feed(html_string)
        except Exception as e:
            print(str(e))
            return set()
        return link_extractor.page_links()

    # Saves queue data to project files
    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if (url in Crawler.queue) or (url in Crawler.crawled):
                continue
            Crawler.queue.add(url)

    @staticmethod
    def get_url_from_code():
        return Crawler.url_from_code

    @staticmethod
    def update_files():
        write_set_to_file(Crawler.queue, Crawler.queue_file)
        write_set_to_file(Crawler.crawled, Crawler.crawled_file)

