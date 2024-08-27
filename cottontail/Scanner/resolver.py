import socket
import logging
from logger import ErrorReporter

def resolve_target_ip(tgt_host):
    """Resolve the target host to an IP address."""
    try:
        tgt_ip = socket.gethostbyname(tgt_host)
        logging.info(f'Scan Results for: {tgt_ip}')
        return tgt_ip
    except socket.gaierror as e:
        ErrorReporter.report_error(f"Cannot resolve '{tgt_host}': Unknown host. Error: {e}")
        return None