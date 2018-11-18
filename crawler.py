# Mirko Mantovani
from urllib.request import urlopen
from link_extractor import LinkExtractor
from domain_utils import *
from crawling_utils import *


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

    def __init__(self, folder, base_url, domain_name):
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
        create_domain_directory(Crawler.folder)
        create_data_files(Crawler.folder, Crawler.base_url)
        Crawler.queue = get_set_from_file(Crawler.queue_file)
        Crawler.crawled = get_set_from_file(Crawler.crawled_file)

    # Updates user display, fills queue and updates files
    @staticmethod
    def crawl_page(thread_name, page_url):
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
            response = urlopen(page_url)
            if 'text/html' in response.getheader('Content-Type'):
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
                if Crawler.save_html_pages:
                    write_file(Crawler.pages_folder+str(len(Crawler.crawled)), html_string)
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
            # if Crawler.domain_name != get_domain_name(url):
            #     continue
            Crawler.queue.add(url)

    @staticmethod
    def update_files():
        write_set_to_file(Crawler.queue, Crawler.queue_file)
        write_set_to_file(Crawler.crawled, Crawler.crawled_file)

