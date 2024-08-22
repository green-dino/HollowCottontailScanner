import unittest
from utils import parse_ports

class TestUtils(unittest.TestCase):

    def test_parse_single_port(self):
        result = parse_ports('80')
        self.assertEqual(result, [80])

    def test_parse_port_range(self):
        result = parse_ports('1000-1003')
        self.assertEqual(result, [1000, 1001, 1002, 1003])

    def test_parse_multiple_ports(self):
        result = parse_ports('80, 443, 8080')
        self.assertEqual(result, [80, 443, 8080])

if __name__ == '__main__':
    unittest.main()
