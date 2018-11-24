# Mirko Mantovani
import threading
from queue import Queue
from crawler import Crawler
from domain_utils import *
from crawling_utils import *

FOLDER = 'uic'
HOMEPAGE = 'https://www.cs.uic.edu/'
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_PATH = FOLDER + '/queue.txt'
CRAWLED_PATH = FOLDER + '/crawled.txt'
THREAD_NUMBER = 20
# The queue module implements multi-producer, multi-consumer queues. It is especially useful in threaded programming
# when information must be exchanged safely between multiple threads.
queue = Queue()
counter = 100
Crawler(FOLDER, HOMEPAGE, DOMAIN_NAME)


def start_crawling():
    create_workers()
    crawl()


# Create worker threads (will die when main exits)
def create_workers():
    for _ in range(THREAD_NUMBER):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Do the next job in the queue
def work():
    # global counter
    # while counter > 0:
    #     counter = counter-1
    while True:
        url = queue.get()
        Crawler.crawl_page(threading.current_thread().name, url)
        queue.task_done()


# Each queued link is a new job
def create_jobs():
    for link in get_set_from_file(QUEUE_PATH):
        queue.put(link)
    queue.join()
    crawl()


# Check if there are items in the queue, if so crawl them
def crawl():
    queued_links = get_set_from_file(QUEUE_PATH)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue')
        create_jobs()


start_crawling()

