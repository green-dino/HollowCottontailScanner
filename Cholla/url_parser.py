import logging
from urllib.parse import urlparse

def parse_url(url):
    parsed_url = urlparse(url)
    
    if parsed_url.scheme not in ('http', 'https'):
        raise ValueError("URL must start with 'http://' or 'https://'")
    
    if not parsed_url.netloc:
        raise ValueError("Invalid URL format: Missing host")
    
    host = parsed_url.netloc
    path = parsed_url.path if parsed_url.path else '/'
    
    logging.info(f"Parsed URL: scheme={parsed_url.scheme}, host={host}, path={path}")
    return host, path