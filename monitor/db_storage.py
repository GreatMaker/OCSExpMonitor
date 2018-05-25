from .__init__ import logger
from . import settings
import sqlite3
import os
import time


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DBStorage(metaclass=Singleton):

    def __init__(self):
        self.database = 'data.db'
        self.conn = None
        self.cursor = None
        self.connected = False
        self.create = False

        if not os.path.exists(self.database):
            self.create = True

        self.connect()
        logger.info("Database connected")

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def connect(self):
        """Connect to the SQLite3 database."""

        self.conn = sqlite3.connect(self.database)
        self.cursor = self.conn.cursor()
        self.connected = True

    def close(self):
        """Close the SQLite3 database."""

        self.conn.commit()
        self.conn.close()
        self.connected = False

    def init_db(self):
        if self.create:
            self.prepare_db()

    def prepare_db(self):
        logger.info("Populating database after first creation")

        # Create table MATERIAL_DATA
        str_sql = 'CREATE TABLE `analysis` ( `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, `datetime` INTEGER'

        for m_data in settings.MATERIAL_DATA:
            str_sql = str_sql + ' ,`{}` TEXT'.format(m_data)

        str_sql = str_sql + ')'

        self.cursor.execute(str_sql)

        str_sql = 'CREATE TABLE `num_data` ( `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, ' \
                  '`analysis_id` INTEGER NOT NULL, `color_class` TEXT NOT NULL'

        for x in range(0, settings.NUM_CLASSES):
            str_sql = str_sql + ' ,`class_{}` INTEGER'.format(x + 1)

        str_sql = str_sql + ')'

        self.cursor.execute(str_sql)

        str_sql = 'CREATE TABLE `size_classes`(`id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, ' \
                  '`num` INTEGER NOT NULL, `name` TEXT NOT NULL)'

        self.cursor.execute(str_sql)

        # Save (commit) the changes
        self.conn.commit()

    def write_data(self, data):
        l_data_time = data[0]
        l_data_material = data[1]
        l_data_header = data[2]
        l_data_numeric = data[3]
        insert_id = 0

        # populate size_classes if needed
        str_sql = 'SELECT count(*) FROM `size_classes`'
        self.cursor.execute(str_sql)
        result = self.cursor.fetchone()

        if result[0] == 0:
            for x in range(0, settings.NUM_CLASSES):
                str_sql = 'INSERT INTO `size_classes` (`num`, `name`) VALUES ({}, \'{}\')'.format(x + 1, l_data_numeric[x][0])
                self.cursor.execute(str_sql)

        str_sql = 'INSERT INTO `analysis` (`datetime`'
        str_data_sql = ' VALUES ({}'.format(time.mktime(l_data_time.timetuple()))

        test = dict(l_data_material)

        for material_field in settings.MATERIAL_DATA:
            str_sql = str_sql + ' ,`{}`'.format(material_field)
            str_data_sql = str_data_sql + ', \'{}\''.format(test[material_field])

        str_sql = str_sql + ')'
        str_data_sql = str_data_sql + ')'

        str_sql = str_sql + str_data_sql

        self.cursor.execute(str_sql)

        insert_id = self.cursor.lastrowid

        str_sql = 'INSERT INTO `num_data` (`analysis_id`, `color_class`'

        index = 1

        for data_header in l_data_header:

            str_sql_l = str_sql
            for x in range(0, settings.NUM_CLASSES):
                str_sql_l = str_sql_l + ' ,`class_{}`'.format(x + 1)

            str_sql_v = ') VALUES ({}, \'{}\''.format(insert_id, data_header)

            for n_data in l_data_numeric:
                str_sql_v = str_sql_v + ', {}'.format(n_data[index])

            str_sql_v = str_sql_v + ')'

            index = index + 1

            self.cursor.execute(str_sql_l + str_sql_v)

        # Save (commit) the changes
        self.conn.commit()
