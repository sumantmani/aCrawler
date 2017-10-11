import argparse
import asyncio
import re
import time
import urllib.parse

import logging

from collections import namedtuple

import aiohttp

from logger import set_up_logging

logger = set_up_logging()

def is_redirect(response):
    return response.status in (300, 301, 302, 303, 307)

def lenient_host(host):
    parts = host.split('.')[-2:]
    return ''.join(parts)

FetchStatistic = namedtuple('FetchStatistic',
                            ['url',
                             'next_url',
                             'status',
                             'exception',
                             'size',
                             'content_type',
                             'encoding',
                             'num_urls',
                             'num_new_urls'])
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
        self.session = aiohttp.ClientSession(loop=self.loop)
        self.root_domains = set()

        for root in roots:
            self.task_queue.add(root)
            continue
            parts = urllib.parse.urlparse(root)
            host, port = urllib.parse.splitport(parts.netloc)
            if not host:
                continue
            if  re.match(r'\A[\d\.]*\Z', host):
                self.root_domains.add(host)
            else:
                host = host.lower()
                if self.strict:
                    self.root_domains.add(host)
                else:
                    self.root_domains.add(lenient_host(host)) # Need to implement it.
            for root in roots:
                self.add_url(root)
            self.t0 = time.time()
            self.t1 = None

    def close(self):
        '''Close resources'''
        self.session.close()

    def host_okay(self, host):
        '''Check if a host should be crawled.

        Long description
        '''
        pass

    def parse_links(self, response):
        '''Return a FetchStatistic and list of links.'''

        links = set()
        content_type = None
        encoding = None
        body = response.read()

        if response.status == 200:
            # or check for all status_ok

            content_type = response.headers.get('content-type')
            pdict = dict()

            if content_type:
                content_type, pdict = cgi.parse_header(content_type)

            encoding = pdict.get('charset', 'utf-8')
            if content_type in ('text/html', 'application/xml'):
                text = response.text()
                
                # Replace href with (?:href|src) to follow image link
                urls = set(re.findall(r'''(?i)href=["']([^\s"'<>]+)''',
                                      text))
                if urls:
                    logger.info('got {} distinct urls form {}.'.format(
                        len(urls), response.url))

                for url in urls:
                    normalized = urllib.parse.urljoin(response.url, url)
                    defragmented, frag = urllib.parse.urldefrag(normalized)
                    if self.url_allowed(defragmented):
                        links.add(defragmentd)

        # will return
        logger.info('links' + str(links))
        return links

    
    def fetch(self, url, max_redirect):
        '''Fetch one URL.'''
        logger.info('inside fetch')        
        tries = 0
        exception = None
        while tries < self.max_tries:
            try:
                response = self.session.get(
                    url, allowed_redirect=False)
                
                if tries > 1:
                    logger.info('try {} for {} success', tries, url)

                break
            except aiohttp.ClientError as client_error:
                logger.info('try {} for {} raised {}.'.
                            format(tries, url, clent_error))
                exception = client_error

            tries += 1
        else:
            # We never broke out of the loop: all tries failed.
            logger.error('{} failed after {} tries.'
                         .format(url, self.max_tries))
            return

        try:
            pass
        finally:
            response.release()

    def work(self):
        '''Process queue items forerver.'''
        try:
            while True:
                url, max_redirect = self.task_queue.get()
                assert url in self.seen_urls
                self.fetch(url, max_redirect)
                self.task_queue.task_done()
        except asyncio.CancelledError:
            pass
    
    def url_allowed(self, url):
        return True
    
    def add_url(self, url, max_redirect=None):
        '''Add a URL to the queue if not seen before.'''
        if max_redirect is None:
            max_redirect = self.max_redirect

        logger.debug('adding {} {}'.format(url, max_redirect))
        self.seen_urls.add(url)
        self.task_queue.put_nowait((url, max_redirect))

    
    def crawl(self):
        '''Run the crawler until all finished.'''
        self.t0 = time.time()
        for task in self.task_queue:
            pass
        self.t1 = time.time()

def main():

    # roots = {fix_url(root) for root in args.roots}
    roots = set(['https://api.yeongmang.com'])

    crawler = Crawler(roots,
                      max_redirect=10,
                      max_tries=10,
                      max_tasks=20,
                     )
    crawler.crawl()
    return

    try:
        loop.run_until_complete(crawler.crawl()) 
    except KeyboardInterrupt:
        sys.stderr.flush()
        print('Interrupted')
    finally:
        crawler.close()

        loop.stop()
        loop.run_forver()

        loop.close()

if __name__ == '__main__':
    main()
