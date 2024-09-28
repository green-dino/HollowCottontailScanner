import unittest
from unittest.mock import patch, MagicMock
from scanner import conn_scan

class TestScanner(unittest.TestCase):

    @patch('scanner.socket.socket')
    @patch('scanner.logging.info')
    def test_conn_scan_open_port(self, mock_info, mock_socket):
        mock_socket_inst = MagicMock()
        mock_socket.return_value = mock_socket_inst
        mock_socket_inst.recv.return_value = b'HTTP/1.1 200 OK'
        
        screen_lock = MagicMock()
        conn_scan('127.0.0.1', 80, screen_lock)

        mock_info.assert_any_call('80/tcp open')
        mock_info.assert_any_call('Response from port 80: HTTP/1.1 200 OK')

    @patch('scanner.socket.socket')
    @patch('scanner.logging.info')
    def test_conn_scan_closed_port(self, mock_info, mock_socket):
        mock_socket_inst = MagicMock()
        mock_socket.return_value = mock_socket_inst
        mock_socket_inst.connect.side_effect = ConnectionRefusedError
        
        screen_lock = MagicMock()
        conn_scan('127.0.0.1', 81, screen_lock)

        mock_info.assert_any_call('81/tcp closed')

if __name__ == '__main__':
    unittest.main()
