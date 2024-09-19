import mysql.connector

class DatabaseConnection:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            port=33,
            user='root',
            password='',
            database='iot'
        )
        self.cursor = self.conn.cursor()

    def execute_query(self, query, params):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.conn.close()