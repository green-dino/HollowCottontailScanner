import logging

def parse_url(url):
    if not url.startswith("http://"):
        raise ValueError("URL must start with 'http://'")
    
    parts = url.split('/')
    if len(parts) < 3:
        raise ValueError("Invalid URL format")
    
    host = parts[2]
    path = '/' + '/'.join(parts[3:]) if len(parts) > 3 else '/'
    
    logging.info(f"Parsed URL: host={host}, path={path}")
    return host, path