import logging
from url_parser import parse_url
from request_sender import send_request
from response_handler import handle_response

# Configure logging
logging.basicConfig(level=logging.INFO)

def fetch_data_from_url(url):
    try:
        host, path = parse_url(url)
        mysock = send_request(host, path)
        response = handle_response(mysock)
        print(response)
    except ValueError as ve:
        logging.error(f"ValueError: {ve}")
    except Exception as e:
        logging.error(f"Error: {e}")

if __name__ == "__main__":
    url = input("Enter the URL: ")
    fetch_data_from_url(url)