import socket
import logging
from logger import ErrorReporter

# Set a default timeout for socket operations
DEFAULT_TIMEOUT = 5
socket.setdefaulttimeout(DEFAULT_TIMEOUT)

def resolve_target_ip(tgt_host):
    """Resolve the target host to an IP address."""
    # Input validation
    if not tgt_host or tgt_host.isspace():
        ErrorReporter.report_error("Target host is empty or invalid.")
        return None

    try:
        # Attempt to resolve the host to an IP address
        tgt_ip = socket.gethostbyname(tgt_host)
        logging.info(f'Resolved {tgt_host} to {tgt_ip}')
        return tgt_ip
    except socket.gaierror as e:
        ErrorReporter.report_error(f"Cannot resolve '{tgt_host}': Unknown host. Error: {e}")
    except socket.herror as e:
        ErrorReporter.report_error(f"Cannot resolve '{tgt_host}': Host error. Error: {e}")
    except socket.timeout as e:
        ErrorReporter.report_error(f"Cannot resolve '{tgt_host}': Timeout occurred. Error: {e}")
    except socket.error as e:
        ErrorReporter.report_error(f"Cannot resolve '{tgt_host}': Socket error. Error: {e}")
    except Exception as e:
        ErrorReporter.report_error(f"An unexpected error occurred: {e}")
    
    return None
