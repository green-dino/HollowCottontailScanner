import socket
import logging
from config import PORT

def send_request(host, path):
    try:
        mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mysock.connect((host, PORT))
        
        cmd = f'GET {path} HTTP/1.0\r\nHost: {host}\r\n\r\n'.encode()
        mysock.send(cmd)
        
        logging.info(f"Request sent to {host}{path}")
        return mysock
    except Exception as e:
        logging.error(f"Error sending request: {e}")
        raise