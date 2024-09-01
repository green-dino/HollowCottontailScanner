def parse_ports(port_ranges: str) -> list[int]:
    """
    Parse a comma-separated list of ports and/or port ranges.
    
    Args:
        port_ranges (str): A string containing ports and/or port ranges 
                           (e.g., "80, 443, 1000-2000, 3001").
    
    Returns:
        list[int]: A list of individual ports parsed from the input string.
    
    Raises:
        ValueError: If any port or port range is invalid.
    """
    ports = set()  # Use a set to avoid duplicates

    if not port_ranges:
        raise ValueError("Port ranges string is empty.")

    for part in port_ranges.split(','):
        part = part.strip()  # Remove any leading/trailing spaces
        if '-' in part:
            try:
                start, end = map(int, part.split('-'))
                if start > end:
                    raise ValueError(f"Invalid port range: {part}. Start port is greater than end port.")
                ports.update(range(start, end + 1))
            except ValueError:
                raise ValueError(f"Invalid port range: {part}. Ensure ports are integers and in the correct format.")
        else:
            try:
                ports.add(int(part))
            except ValueError:
                raise ValueError(f"Invalid port: {part}. Ensure the port is an integer.")
    
    return sorted(ports)  # Return a sorted list of ports