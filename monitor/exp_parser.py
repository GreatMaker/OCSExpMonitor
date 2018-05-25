from .__init__ import logger
from . import settings
import mmap
import re
from datetime import datetime


class ExpParser:
    def __init__(self, file_path):
        self.path = file_path
        self.date_time = None
        self.material_data = []
        self.header = []
        self.numerical_data = []

    def get_data(self):
        return self.date_time, self.material_data, self.header, self.numerical_data

    def parse_data(self):
        with open(self.path, 'rb', 0) as file, mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as s:
            self.parse_datetime(s)
            self.parse_material_data(s)
            self.parse_numerical_data(s)

    def parse_datetime(self, data):
        # find start time
        start = data.find(b'Start')

        if start != -1:
            end = data.find(b'\r', start)
            colon = data.find(b':', start)

            if colon != -1:
                s_date = data[colon + 1: end].decode("utf-8").lstrip(' ')
                self.date_time = datetime.strptime(s_date, '%I:%M:%S %p %m/%d/%Y')

    def parse_material_data(self, data):

        for material_field in settings.MATERIAL_DATA:
            # find start of string
            start = data.find(material_field.encode('utf-8'))

            if start != -1:
                end = data.find(b'\r', start)
                colon = data.find(b':', start)

                if colon != -1:
                    s_field = data[colon + 1: end].decode("utf-8").strip(' ')
                    self.material_data.append((material_field, s_field))

    def parse_numerical_data(self, data):
        # find start time
        start = data.find(b'Size /')
        end = data.find(b'\r', start)

        if start != -1 and end != -1:
            # self.header = ['Size'] + data[start + 8: end].decode("utf-8").split()
            self.header = data[start + 8: end].decode("utf-8").split()

        for x in range(0, settings.NUM_CLASSES):
            start = end + 2
            end = data.find(b'\r', start)

            if end != -1:
                self.numerical_data.append(re.split(r'\t+', data[start: end].decode("utf-8")))
