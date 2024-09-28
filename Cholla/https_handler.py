import ssl
import socket
import logging

def send_https_request(host, path):
    context = ssl.create_default_context()
    with socket.create_connection((host, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=host) as ssock:
            request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
            ssock.sendall(request.encode())
            response = ssock.recv(4096)
            return response

def handle_https_response(response):
    return response.decode()

# Configure logging
logging.basicConfig(level=logging.INFO)

def fetch_data_from_url(url):
    try:
        host, path = parse_url(url)
        if url.startswith("https://"):
            response = send_https_request(host, path)
            response = handle_https_response(response)
        else:
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