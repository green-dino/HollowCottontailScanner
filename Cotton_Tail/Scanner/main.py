from resolver import resolve_target_ip
from scanner import port_scan
from logger import ErrorReporter

def main():
    """Main function to run the port scanner."""
    try:
        tgt_host = input("Enter the target host address: ")
        tgt_ports = input("Enter the target port[s] separated by comma or range (e.g., 80, 443, 1000-2000): ")
        if not (tgt_host and tgt_ports):
            ErrorReporter.report_error('You must specify a target host and port[s].')
            return

        tgt_ports = [port.strip() for port in tgt_ports.split(',')]  # Trim spaces around each port/range
        tgt_ip = resolve_target_ip(tgt_host)
        if tgt_ip:
            port_scan(tgt_ip, tgt_ports)
    except KeyboardInterrupt:
        ErrorReporter.report_error("User interrupted the scan.")
        exit(0)

if __name__ == '__main__':
    main()
