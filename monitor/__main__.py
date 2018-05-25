from . import settings
from . import monitoring
from . import db_storage
from .__init__ import logger
import argparse
import configparser
from pathlib import Path
import ast
import signal

monitoring_thread = None


def signal_handler(signal, frame):
    logger.info("%s stopping" % settings.PROG_NAME)
    monitoring_thread.end_monitoring()


def parse_config_file(cfg_file):
    try:
        config = configparser.ConfigParser()
        config.read(cfg_file)

        settings.DATA_PATH = config.get('DATA', 'path')
        settings.MATERIAL_DATA = ast.literal_eval(config.get("MATERIAL_DATA_FIELDS", "fields"))
        settings.NUM_CLASSES = config.getint('SIZE_CLASSES', 'num_classes')

        if len(settings.MATERIAL_DATA) == 0:
            logger.error("no data in fields parameter")
            return False
    except configparser.Error as err:
        logger.error("error parsing config file: %s" % err)
        return False
    else:
        return True


if __name__.endswith('__main__'):

    # signal handler
    signal.signal(signal.SIGINT, signal_handler)

    # parse command line arguments
    parser = argparse.ArgumentParser(description='Process config file argument')
    parser.add_argument('--config', dest='config_file_path', default='config.cfg',
                        help='Configuration file for the program')
    args = parser.parse_args()

    logger.info("%s started" % settings.PROG_NAME)
    logger.info("running with the following config file: %s" % args.config_file_path)

    # config file
    config_file = Path(args.config_file_path)

    # check existence of file
    if config_file.is_file():
        # parse config file
        ret = parse_config_file(args.config_file_path)

        if ret:
            monitoring_thread = monitoring.MonitoringThread()

            monitoring_thread.start()
            monitoring_thread.join()
    else:
        logger.error("%s file not found" % args.config_file_path)
