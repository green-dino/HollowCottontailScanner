def parse_ports(port_range):
    """Parse a single port or a range of ports."""
    try:
        if '-' in port_range:
            start, end = map(int, port_range.split('-'))
            return list(range(start, end + 1))
        else:
            return [int(port_range)]
    except ValueError as e:
        raise ValueError(f"Invalid port range: {port_range}") from e