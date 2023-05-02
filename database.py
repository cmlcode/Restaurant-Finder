import psycopg2
from config import config
from restaurant import Restaurant

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

    def connect(self, database_name: str, username: str, user_password: str, database_port = 5432, database_host = "localhost") -> None:
        self.conn = psycopg2.connect(
            host = database_host,
            database = database_name,
            user = username,
            password = user_password,
            port = database_port
        )
    def add_restaurant(self, restaurant: Restaurant):
        input_command = f"""INSERT INTO restaurants(name,type,rating,price,reviews,latitude,longitude)
        VALUES (
            '{restaurant.name.lower()}',
            '{restaurant.food_type.lower()}',
            '{restaurant.rating}',
            '{restaurant.price}',
            '{restaurant.reviews}',
            '{restaurant.loc[0]}',
            '{restaurant.loc[1]}'
        )
        RETURNING restaurant_id;
        """
        restaurant_id = None

        try:
            cur = self.conn.cursor()
            cur.execute(input_command)
            restaurant_id = cur.fetchone()[0]
            self.conn.commit()
            cur.close()
        except(Exception, psycopg2.DatabaseError) as error:
            print(f"ERROR: Can't add restaurant to database: {error}")

        return restaurant_id
