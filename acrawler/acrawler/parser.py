'''
Parser job is to parse links from response.

'''
from bs4 import BeautifulSoup

import logging

logger = logging.getLogger(__name__)

class Parser:
    pass

class DefaultParser(Parser):
    '''Default Parser'''

    def __init__(self):
        pass

    def parse_link(self, resp):
        soup = BeautifulSoup(resp, 'html.parser')

        for a in soup.find_all('a', href=True):
            yield a['href']
