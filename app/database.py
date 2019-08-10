import sqlite3
from app.config import db_file


class DataBase:
    connect = sqlite3.connect(db_file, check_same_thread=False)
    cursor = connect.cursor()

    def __init__(self):
        if not self.select():
            self.insert('USD')

    def select(self):
        return [row[0] for row in self.cursor.execute('SELECT name FROM currency')]

    def insert(self, _value):
        self.cursor.execute('INSERT INTO currency(name) VALUES (\'{}\')'.format(_value))
        self.connect.commit()

    def __del__(self):
        self.connect.close()
