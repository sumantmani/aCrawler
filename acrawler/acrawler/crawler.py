import time
import logging

from parser import DefaultParser
from fetcher import DefaultFetcher, HttpsFetcher
from logger import set_up_logging

logger = set_up_logging()

class Crawler:
    '''Crawl a set to urls.

    Long description
    '''

    def __init__(self, roots,
                exclude=None, strict=True,
                max_redirect=10, max_tries=4,
                max_tasks=10, loop=None):
        #self.loop = loop or asyncio.get_event_loop()
        self.roots = roots
        self.exclude = exclude
        self.strict = strict
        self.max_redirect = max_redirect
        self.max_tries = max_tries
        self.max_tasks = max_tasks
        self.task_queue = set() # asyncio.Queue(loop=self.loop)
        self.seen_urls = set()
        self.done = []
        self.root_domains = set()

        self.fetcher = DefaultFetcher()
        self.parser = DefaultParser()

        self.t0 = time.time()
        self.t1 = None


    def work(self):
        '''Process queue items forerver.'''
        try:
            while True:
                url, max_redirect = self.task_queue.get()
                assert url in self.seen_urls
                #self.fetch(url, max_redirect)
                #self.task_queue.task_done()
        except asyncio.CancelledError:
            pass
    
    
    def crawl(self):
        '''Run the crawler until all finished.'''
        self.t0 = time.time()
        for task in range(1): #self.task_queue:
            resp = self.fetcher.fetch('https://stackoverflow.com', 443)
            #self.validate_response(resp)
            new_urls = self.parser.parse_link(resp)
            print('new urls', list(new_urls))
        self.t1 = time.time()

def main():

    # roots = {fix_url(root) for root in args.roots}
    roots = set(['https://api.yeongmang.com'])

    crawler = Crawler(roots,
                      max_redirect=10,
                      max_tries=10,
                      max_tasks=20,
                     )
    try:
        crawler.crawl()
    except KeyboardInterrupt:
        sys.stderr.flush()
        print('Interrupted')


if __name__ == '__main__':
    main()
