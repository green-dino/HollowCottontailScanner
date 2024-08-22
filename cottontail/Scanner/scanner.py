import socket
from threading import Semaphore
from concurrent.futures import ThreadPoolExecutor
from logger import ErrorReporter
from utils import parse_ports

# Constants
TIMEOUT = 1
SCAN_MESSAGE = b'CottonTailScanner\r\n'
MAX_THREADS = 100

def conn_scan(tgt_host, tgt_port, screen_lock):
    """Connect and scan a specific port."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn_skt:
            conn_skt.settimeout(TIMEOUT)
            conn_skt.connect((tgt_host, tgt_port))
            conn_skt.send(SCAN_MESSAGE)
            results = conn_skt.recv(100)
            with screen_lock:
                logging.info(f'{tgt_port}/tcp open')
                logging.info(f'Response from port {tgt_port}: {results.decode("utf-8", errors="ignore")}')
    except (ConnectionRefusedError, socket.timeout):
        with screen_lock:
            logging.info(f'{tgt_port}/tcp closed')
    except Exception as e:
        with screen_lock:
            ErrorReporter.report_error(str(e))

def port_scan(tgt_host, tgt_ports):
    """Perform a port scan on the target host."""
    screen_lock = Semaphore(value=1)

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        for port_range in tgt_ports:
            ports = parse_ports(port_range)
            for port in ports:
                executor.submit(conn_scan, tgt_host, port, screen_lock)
