import logging
import sys

root_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

root_handler = logging.StreamHandler(sys.stdout)
root_handler.setLevel(logging.INFO)
root_handler.setFormatter(root_formatter)

root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
root_logger.addHandler(root_handler)


def init_app(app):
    testing = app.config['TESTING']
    app.logger.addHandler(root_handler)
    if testing:
        app.logger.info('App is configured for testing')
        app.logger.setLevel(logging.DEBUG)
