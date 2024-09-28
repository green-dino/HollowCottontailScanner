import unittest
from unittest.mock import patch
from resolver import resolve_target_ip

class TestResolver(unittest.TestCase):

    @patch('resolver.socket.gethostbyname')
    @patch('resolver.logging.info')
    def test_resolve_target_ip_success(self, mock_info, mock_gethostbyname):
        mock_gethostbyname.return_value = '192.168.1.1'
        ip = resolve_target_ip('example.com')
        self.assertEqual(ip, '192.168.1.1')
        mock_info.assert_called_once_with('Scan Results for: 192.168.1.1')

    @patch('resolver.socket.gethostbyname')
    @patch('resolver.ErrorReporter.report_error')
    def test_resolve_target_ip_failure(self, mock_report_error, mock_gethostbyname):
        mock_gethostbyname.side_effect = socket.gaierror
        ip = resolve_target_ip('nonexistent.com')
        self.assertIsNone(ip)
        mock_report_error.assert_called_once_with("Cannot resolve 'nonexistent.com': Unknown host")

if __name__ == '__main__':
    unittest.main()
