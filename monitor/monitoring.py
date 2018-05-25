from . import settings
from . import exp_parser
from . import xls_output
from . import db_storage
from .__init__ import logger
import os
import time
from threading import Lock, Thread

poll_run_flag = True


class MonitoringThread(Thread):
    def __init__(self):
        super(MonitoringThread, self).__init__()

        self.before = dict([(f, None) for f in os.listdir(settings.DATA_PATH)])
        self.after = None
        self.poll_run_flag = True
        self.lock = Lock()

    def end_monitoring(self):
        self.lock.acquire()
        self.poll_run_flag = False
        self.lock.release()

    def run(self):
        logger.info("starting with monitoring folder %s" % settings.DATA_PATH)

        # start database connection
        db_storage.DBStorage()

        while 1:
            self.after = dict([(f, None) for f in os.listdir(settings.DATA_PATH)])

            added = [f for f in self.after if f not in self.before]

            if added:
                if added[0].lower().endswith('.exp'):
                    logger.info("EXP file added %s" % os.path.join(settings.DATA_PATH, added[0]))

                    # run parser
                    parser = exp_parser.ExpParser(os.path.join(settings.DATA_PATH, added[0]))
                    parser.parse_data()

                    logger.info("EXP file processed")

                    # export su DB
                    db = db_storage.DBStorage()
                    db.init_db()

                    db.write_data(parser.get_data())

                    xml_out = xls_output.XlsOutput(parser.get_data())
                    xml_out.save()

            self.before = self.after

            self.lock.acquire()

            if not self.poll_run_flag:
                self.lock.release()
                break

            self.lock.release()
            time.sleep(10)


def monitoring_routine():
    before = dict([(f, None) for f in os.listdir(settings.DATA_PATH)])

    while 1:
        time.sleep(10)

        after = dict([(f, None) for f in os.listdir(settings.DATA_PATH)])

        added = [f for f in after if f not in before]

        # found added file
        if added:
            print("Added: ", ", ".join(added))

        before = after

        # interrupt thread
        if not poll_run_flag:
            break
