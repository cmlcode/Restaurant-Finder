import psycopg2
from config import config

class Database:
    def __init__(self) -> None:
        #Based off of POSTGRESQL Tutorial: https://www.postgresqltutorial.com/postgresql-python/connect/
        self.conn = None
        try:
            #Read connection params
            params = config()

            #Connect to PostgreSQL server
            print('Connecting to the PostgreSQL database')
            self.conn = psycopg2.connect(**params)

            #Create a cursor
            cur = self.conn.cursor()

            #Execute statement
            cur.execute('SELECT version()')

            #Display PostgreSQL database version
            db_version = cur.fetchone()
            print(f"PostgreSQL databse version: {db_version}")

            #Close server communication
            cur.close()
        except(Exception, psycopg2.DatabaseError) as error:
            print(f"ERROR: Can't connect to database: {error}")

    def connect(self, database_name, username, user_password, database_port = 5432, database_host = "localhost") -> None:
        self.conn = psycopg2.connect(
            host = database_host,
            database = database_name,
            user = username,
            password = user_password,
            port = database_port
        )