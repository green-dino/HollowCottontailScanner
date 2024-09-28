import logging
from request import Request, Response
from protocol_handler import ProtocolHandler
import socket

# Configure logging
logging.basicConfig(level=logging.INFO)

def fetch_data_from_url(url, method='GET', body=None):
    try:
        request = Request(url, method, body)
        handler = ProtocolHandler(request)
        raw_response = handler.send_request()
        response = Response(raw_response)
        print(response.handle())
    except ValueError as ve:
        logging.error(f"ValueError: {ve}")
    except socket.error as se:
        logging.error(f"Socket error: {se}")
    except ssl.SSLError as ssle:
        logging.error(f"SSL error: {ssle}")
    except Exception as e:
        logging.error(f"Error: {e}")

if __name__ == "__main__":
    url = input("Enter the URL: ")
    method = input("Enter the HTTP method (GET, POST, DELETE, etc.): ")
    body = None
    if method in ['POST', 'PUT', 'PATCH']:
        body = input("Enter the request body: ")
    fetch_data_from_url(url, method, body)