# Mirko Mantovani
from html.parser import HTMLParser
from urllib import parse
from domain_utils import *


class LinkExtractor(HTMLParser):

    def __init__(self, base_url, page_url, restrict_to_domain=True, domain='uic.edu'):
        super().__init__()
        self.base_url = base_url
        self.page_url = page_url
        self.exclude = (".docx", ".doc",  ".avi", ".mp4", ".jpg", ".jpeg", ".png", ".gif", ".pdf",
                        ".gz", ".rar", ".tar", ".tgz", ".zip", ".exe", ".js", ".css", ".ppt")
        self.restrict_to_domain = restrict_to_domain
        self.domain = domain
        self.links = set()

    # Callback function that handles the opening of a <a> tag while parsing the html
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (attribute, value) in attrs:
                if attribute == 'href':
                    url = parse.urljoin(self.base_url, value)
                    if not url.lower().endswith(self.exclude):
                        # Stripping query string in link
                        url = url.split('#')[0]
                        url = url.split('?', maxsplit=1)[0]
                        # Stripping trailing slashes
                        url = url.rstrip('/')
                        url = url.strip()
                        url = url.split('<')[0]
                        spl = url.split(':')
                        if len(spl) == 2 and spl[0] == 'http':
                            url = spl[0]+'s:'+spl[1]
                        if url and self.restrict_to_domain and self.is_in_domain(url):
                            self.links.add(url)

    def page_links(self):
        return self.links

    def error(self, message):
        print('Error in link extractor')

    def is_in_domain(self, url):
        if get_domain_name(url) == self.domain:
            return True
        else:
            return False
