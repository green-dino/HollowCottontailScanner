import logging
import socket
import ssl
from urllib.parse import urlparse

class Request:
    def __init__(self, url, method='GET', body=None):
        self.url = url
        self.method = method
        self.body = body
        self.parsed_url = urlparse(url)
        self.host = self.parsed_url.netloc
        self.path = self.parsed_url.path if self.parsed_url.path else '/'
        self.scheme = self.parsed_url.scheme

    def prepare(self):
        request_line = f"{self.method} {self.path} HTTP/1.1\r\n"
        headers = f"Host: {self.host}\r\nConnection: close\r\n"
        if self.body:
            headers += f"Content-Length: {len(self.body)}\r\n"
        headers += "\r\n"
        return request_line + headers + (self.body if self.body else '')

class Response:
    def __init__(self, raw_response):
        self.raw_response = raw_response

    def handle(self):
        return self.raw_response.decode()