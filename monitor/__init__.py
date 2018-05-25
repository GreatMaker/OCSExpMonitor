# __all__ = ['submodule1', 'submodule2']
__author__ = 'Andrea Visinoni <a.visinoni@fkv.it>'
__version__ = '0.1'

from . import settings
import sys, os, logging

# errors
UNKNOWN_ERROR = -1

# logging
logger = logging.getLogger(settings.PROG_NAME)
if not logger.handlers:

    # create a file handler
    handler = logging.FileHandler(os.path.join(settings.logs_folder, '%s.log' % settings.PROG_NAME))
    console_handler = logging.StreamHandler()

    # setting right level of logging verbosity
    logger.setLevel(settings.LOGGING_VERBOSITY)
    handler.setLevel(settings.LOGGING_VERBOSITY)
    console_handler.setLevel(settings.LOGGING_VERBOSITY)

    # create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(handler)
    logger.addHandler(console_handler)
