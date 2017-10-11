'''
Fetcher class
'''

import socket
import ssl

import logging

logger = logging.getLogger(__name__)


class Fetcher:
    pass

class DefaultFetcher(Fetcher):
    def __init__(self):
        self.sock = socket.socket()
        self.respone = b''

    def fetch(self, url, port):
        import urllib.request
        with urllib.request.urlopen(url) as u:
            resp = u.read()
            return resp
        self.sock.connect((url, port))
        request = 'GET {} HTTP/1.0\r\nHost: {}\r\n\r\n'.format(url)
        self.sock.send(request.encode('ascii'))

        chunk = sock.recv(4096)
        while chunk:
            self.response += chunk
            chunk = sock.recv(4096)

        return self.response

class HttpsFetcher(Fetcher):
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ssock = ssl.wrap_socket(self.sock, ssl_version=ssl.PROTOCOL_TLSv1)
        self.response = b''

    def fetch(self, url, port):
        addr = (url, port)
        self.ssock.connect(addr)
        request = 'GET {} HTTP/1.0\r\nHost: {}\r\n\r\n'.format(url, host)
        self.ssock.send(request.encode('ascii'))

        chunk = ssock.recv(4096)
        while chunk:
            self.response += chunk
            chunk = self.ssock.recv(4096)

        return self.response


class AsyncFetcher(Fetcher):
    def __init__(self):
        pass
    
    def fetch(self):
        self.sock = socket.socket()
        self.sock.setblocking(False)

        try:
            self.sock.connect(('xkcd.com', 80))
        except BlockingIOError:
            pass

        selector.register(self.sock.fileno(),
                          EVENT_WRITE,
                          self.connected)

    def connected(self, key, mask):
        print('connected')
        
        selector.unregister(key.fd)
        request = 'GET {}'.format(self.url)
        self.sock.send(request.encode('ascii'))

        # Register the next callback.
        selector.register(key.fd,
                          EVENT_READ,
                          self.read_response)

    def read_response(self, key, mask):
        global stopped

        chunk = self.sock.recv(4096) # 4k chunk size
        if chunk:
            self.response += chunk
        else:
            selector.unregister(key.fd) # Done reading
            links = self.parse_links()

            for link in links.defference(seen_urls):
                urls_todo.add(link)
                Fetcher(link).fetch() # New Fetcher.

            seen_urls.update(links)
            urls_todo.remove(self.url)
            if not urls_todo:
                stopped = True
