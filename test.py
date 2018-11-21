# url = 'http://admissions.uic.edu/apply-now'
#
# url =url.split('?', maxsplit=1)[0]
# print(url.rstrip('/'))
# url = '      '

# url = url.strip()
#
# if url:
#     print(url)

from multithreaded_crawling import start_crawling
from selectolax.parser import HTMLParser
import time
from urllib.request import urlopen

# start_crawling()

import easygui

# ciao = easygui.ynbox('Shall I continue?', 'Title', ('Yes', 'No'))
# print(ciao)
# easygui.enterbox("ciao","vdf")
# ciao = easygui.msgbox('This is a basic message box.', 'Title Goes Here')
# print(ciao)
# ciao = easygui.buttonbox('Click on your favorite flavor.', 'Favorite Flavor', ('Chocolate', 'Vanilla', 'Strawberry'))
# print(ciao)
# import pickle
# with open('url_from_code_dict.pickle', 'rb') as handle:
#     url_from_code = pickle.load(handle)
# with open('code_from_url_dict.pickle', 'rb') as handle:
#     code_from_url = pickle.load(handle)

# print(url_from_code[1261])
# print(url_from_code[1408])
# print(url_from_code[2183])
# print(url_from_code[3650])
# print(url_from_code[8791])
# print(url_from_code[9658])
# print(url_from_code[10663])

# print(url_from_code[12])
# print(code_from_url['https://www.cs.uic.edu/bin/rdiff/Troy/WebTopicList#_foo=1'])

# print(url_from_code)

# url = 'https://www.cs.uic.esdfFDSDFDFdu/bin/rd#iff/Troy/WebTopicLis.PDF'
# exclude = (".docx", ".doc",  ".avi", ".mp4", ".jpg", ".jpeg", ".png", ".gif", ".GIF", ".pdf",
#                         ".gz", ".rar", ".tar", ".tgz", ".zip", ".exe", ".js", ".css")
# # url = url.split('#')[0]
# print(url)
# print('www.example.com'.strip('w'))
#
# if not url.lower().endswith(exclude):
#     print('good')
# print(url)


