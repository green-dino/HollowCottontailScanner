import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

class ErrorReporter:
    @staticmethod
    def report_error(error):
        logging.error(error)
