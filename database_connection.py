import mysql.connector

class DatabaseConnection:
    """
    This class manages a connection to a MySQL database and provides methods to execute queries
    and handle database resources like cursors and connections.

    Attributes:
        conn: The connection object to the MySQL database.
        cursor: A cursor object used to execute SQL queries and fetch results.
    """

    def __init__(self):
        """
        Initializes the database connection and sets up the cursor.
        The connection is made to a local MySQL database using hardcoded credentials.
        """
        self.conn = mysql.connector.connect(
            host='localhost',    # Hostname of the MySQL server (localhost in this case).
            port=33,             # Port number for the MySQL connection.
            user='root',         # Username for MySQL connection (default 'root').
            password='',         # Password for MySQL connection (empty string for no password).
            database='iot'       # Name of the database to connect to ('iot' in this case).
        )
        self.cursor = self.conn.cursor()  # Creates a cursor object to execute SQL queries.

    def execute_query(self, query, params):
        """
        Executes a given SQL query with the specified parameters and returns the result.

        Args:
            query (str): The SQL query to be executed.
            params (tuple): The parameters to be used in the SQL query.

        Returns:
            list: The result of the query, which is fetched using the cursor.
        """
        self.cursor.execute(query, params)  # Executes the query with the provided parameters.
        return self.cursor.fetchall()       # Fetches and returns all the resulting rows.

    def close(self):
        """
        Closes the cursor and the database connection.
        This method should be called when the database connection is no longer needed.
        """
        self.cursor.close()  # Closes the cursor object.
        self.conn.close()    # Closes the connection to the MySQL database.