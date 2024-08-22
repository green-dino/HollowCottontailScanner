# CottonTailScanner

## Overview

**CottonTailScanner** is a simple, multithreaded port scanner written in Python. It allows users to resolve target hostnames to IP addresses, scan specified ports, and log the results. The application is modular, separating concerns across multiple scripts for better maintainability and flexibility.

## Features

- **Hostname Resolution**: Resolves a target hostname to its corresponding IP address.
- **Port Scanning**: Scans a range of ports to determine if they are open or closed.
- **Multithreading**: Utilizes multithreading to efficiently scan multiple ports simultaneously.
- **Logging**: Logs detailed scan results and errors.

## Project Structure

- `logger.py`: Handles logging configurations and error reporting.
- `resolver.py`: Contains the logic for resolving hostnames to IP addresses.
- `scanner.py`: Includes the main scanning logic and connection attempts.
- `utils.py`: Contains utility functions such as parsing port ranges.
- `main.py`: The entry point for the application, integrating all components.


## Example

```sh
$ python main.py
Enter the target host address: example.com
Enter the target port[s] separated by comma or range (e.g., 80, 443, 1000-2000): 80, 443, 1000-2000
[INFO] Scan Results for: 93.184.216.34
[INFO] 80/tcp open
[INFO] Response from port 80: HTTP/1.1 200 OK
[INFO] 443/tcp closed
```