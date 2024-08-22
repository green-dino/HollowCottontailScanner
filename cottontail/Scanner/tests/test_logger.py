import unittest
from unittest.mock import patch
import logging
from logger import ErrorReporter

class TestLogger(unittest.TestCase):

    @patch('logger.logging.error')
    def test_report_error(self, mock_error):
        ErrorReporter.report_error("Test error message")
        mock_error.assert_called_once_with("Test error message")

if __name__ == '__main__':
    unittest.main()
