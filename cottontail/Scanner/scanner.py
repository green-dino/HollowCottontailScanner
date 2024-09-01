import socket
import logging
from threading import Semaphore, Lock
from concurrent.futures import ThreadPoolExecutor, as_completed
from logger import ErrorReporter
from scan_utils import parse_ports

# Constants
TIMEOUT = 1
SCAN_MESSAGE = b'CottonTailScanner\r\n'
MAX_THREADS = 100
RETRY_COUNT = 3

def validate_ports(ports):
    """
    Validate a list of port numbers, ensuring they fall within the valid range (0-65535).

    Args:
        ports (list): A list of port numbers to validate.

    Returns:
        list: A list of valid port numbers that fall within the range 0-65535.

    Logs:
        - A warning for any port number that is out of the valid range.
    """
    valid_ports = []
    for port in ports:
        if 0 <= port <= 65535:
            valid_ports.append(port)
        else:
            logging.warning(f'Invalid port number: {port}')
    return valid_ports

def conn_scan(tgt_host, tgt_port, screen_lock, protocol='tcp'):
    """
    Attempt to connect and scan a specific port on the target host using the specified protocol.

    Args:
        tgt_host (str): The target host to scan (IP address or hostname).
        tgt_port (int): The target port number to scan.
        screen_lock (threading.Lock): A lock object to ensure thread-safe logging.
        protocol (str, optional): The protocol to use for scanning ('tcp' or 'udp'). Defaults to 'tcp'.

    Returns:
        str: The status of the port after scanning ('open', 'closed', or 'error').

    Logs:
        - Information about open ports and the responses received (for TCP).
        - Information about closed ports or errors encountered during scanning.

    Exceptions:
        - Handles `ConnectionRefusedError`, `socket.timeout`, and general exceptions.
        - Retries the connection attempt up to `RETRY_COUNT` times if a connection fails.
    """
    attempt = 0
    while attempt < RETRY_COUNT:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM if protocol == 'tcp' else socket.SOCK_DGRAM) as conn_skt:
                conn_skt.settimeout(TIMEOUT)
                conn_skt.connect((tgt_host, tgt_port))
                if protocol == 'tcp':
                    conn_skt.send(SCAN_MESSAGE)
                    results = conn_skt.recv(100)
                with screen_lock:
                    logging.info(f'{tgt_port}/{protocol} open')
                    if protocol == 'tcp':
                        logging.info(f'Response from port {tgt_port}: {results.decode("utf-8", errors="ignore")}')
                return 'open'
        except (ConnectionRefusedError, socket.timeout):
            attempt += 1
        except Exception as e:
            with screen_lock:
                ErrorReporter.report_error(str(e))
            return 'error'
    with screen_lock:
        logging.info(f'{tgt_port}/{protocol} closed')
    return 'closed'

def port_scan(tgt_host, tgt_ports, protocol='tcp'):
    """
    Perform a port scan on the target host across a range of ports using the specified protocol.

    Args:
        tgt_host (str): The target host to scan (IP address or hostname).
        tgt_ports (str or list): The target ports to scan. Can be a comma-separated string or a list of port numbers.
        protocol (str, optional): The protocol to use for scanning ('tcp' or 'udp'). Defaults to 'tcp'.

    Returns:
        dict: A dictionary with the scan results categorized as 'open', 'closed', or 'error'.

    The dictionary structure is:
        {
            'open': [list of open ports],
            'closed': [list of closed ports],
            'error': [list of ports that encountered errors during scanning]
        }

    Logs:
        - Errors for invalid ports or when there are no valid ports to scan.
        - Errors encountered during the execution of the scan.

    Exceptions:
        - Handles `KeyboardInterrupt` to allow for graceful shutdown on user interruption.
    """
    screen_lock = Lock()
    results = {'open': [], 'closed': [], 'error': []}

    # Ensure tgt_ports is a string before passing to parse_ports
    if isinstance(tgt_ports, list):
        tgt_ports = ', '.join(tgt_ports)

    valid_ports = validate_ports(parse_ports(tgt_ports))
    if not valid_ports:
        ErrorReporter.report_error('No valid ports to scan.')
        return results

    max_threads = min(MAX_THREADS, len(valid_ports))
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        future_to_port = {executor.submit(conn_scan, tgt_host, port, screen_lock, protocol): port for port in valid_ports}
        try:
            for future in as_completed(future_to_port):
                port = future_to_port[future]
                try:
                    result = future.result()
                    results[result].append(port)
                except Exception as e:
                    ErrorReporter.report_error(f'Error scanning port {port}: {e}')
                    results['error'].append(port)
        except KeyboardInterrupt:
            ErrorReporter.report_error("User interrupted the scan.")
            executor.shutdown(wait=False)
            raise

    return results
