import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

class ErrorReporter:
    @staticmethod
    def report_info(message):
        logging.info(message)

    @staticmethod
    def report_warning(message):
        logging.warning(message)

    @staticmethod
    def report_error(error):
        logging.error(error)

    @staticmethod
    def report_critical(error):
        logging.critical(error)