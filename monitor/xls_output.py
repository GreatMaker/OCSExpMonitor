from .__init__ import logger
from . import settings
import xlsxwriter


class XlsOutput:
    def __init__(self, data):
        self.workbook = xlsxwriter.Workbook('DB.xlsx')
        pass

    def save(self):
        pass
