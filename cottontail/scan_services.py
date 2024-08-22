import socket
from concurrent.futures import ThreadPoolExecutor
from threading import Semaphore
import logging

# Constants
TIMEOUT = 1
SCAN_MESSAGE = b'CottonTailScanner\r\n'
MAX_THREADS = 100

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

class ErrorReporter:
    @staticmethod
    def report_error(error):
        logging.error(error)

def resolve_target_ip(tgt_host):
    """Resolve the target host to an IP address."""
    try:
        tgt_ip = socket.gethostbyname(tgt_host)
        logging.info(f'Scan Results for: {tgt_ip}')
        return tgt_ip
    except socket.gaierror:
        ErrorReporter.report_error(f"Cannot resolve '{tgt_host}': Unknown host")
        return None

def parse_ports(port_range):
    """Parse a single port or a range of ports."""
    if '-' in port_range:
        start, end = map(int, port_range.split('-'))
        return range(start, end + 1)
    else:
        return [int(port_range)]

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
    tgt_ip = resolve_target_ip(tgt_host)
    if not tgt_ip:
        return

    screen_lock = Semaphore(value=1)

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        for port_range in tgt_ports:
            ports = parse_ports(port_range)
            for port in ports:
                executor.submit(conn_scan, tgt_ip, port, screen_lock)

def main():
    """Main function to run the port scanner."""
    try:
        tgt_host = input("Enter the target host address: ")
        tgt_ports = input("Enter the target port[s] separated by comma or range (e.g., 80, 443, 1000-2000): ").split(', ')
        if not (tgt_host and tgt_ports):
            ErrorReporter.report_error('You must specify a target host and port[s].')
            return

        port_scan(tgt_host, tgt_ports)
    except KeyboardInterrupt:
        ErrorReporter.report_error("User interrupted the scan.")
        exit(0)

if __name__ == '__main__':
    main()
