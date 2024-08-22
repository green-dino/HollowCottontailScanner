def parse_ports(port_range):
    """Parse a single port or a range of ports."""
    if '-' in port_range:
        start, end = map(int, port_range.split('-'))
        return range(start, end + 1)
    else:
        return [int(port_range)]
