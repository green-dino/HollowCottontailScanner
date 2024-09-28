import socket
import ssl
import logging

class ProtocolHandler:
    def __init__(self, request):
        self.request = request

    def send_request(self):
        if self.request.scheme == 'https':
            return self._send_https_request()
        else:
            return self._send_http_request()

    def _send_http_request(self):
        with socket.create_connection((self.request.host, 80)) as sock:
            sock.sendall(self.request.prepare().encode())
            response = sock.recv(4096)
            return response

    def _send_https_request(self):
        context = ssl.create_default_context()
        with socket.create_connection((self.request.host, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=self.request.host) as ssock:
                ssock.sendall(self.request.prepare().encode())
                response = ssock.recv(4096)
                return response