"""This database connection file"""
import psycopg2
import psycopg2.extras as roy


class Database:
    """This class connects to the database"""
    def __init__(self, database_url):
        db = database_url

        self.conn = psycopg2.connect(
            database=db, user="postgres", password="root",
            host="localhost", port="5432"
        )
        self.conn.autocommit = True
        self.cur = self.conn.cursor(cursor_factory=roy.RealDictCursor)

    def create_tables(self):
        """method for creating all tables"""
        commands = (
            """CREATE TABLE IF NOT EXISTS users(
                user_id SERIAL PRIMARY KEY,
                username VARCHAR NOT NULL,
                email VARCHAR NOT NULL,
                password VARCHAR NOT NULL
            )""",
            """CREATE TABLE IF NOT EXISTS orders(
                parcel_order_id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                destination VARCHAR NOT NULL,
                receiver_name VARCHAR NOT NULL,
                parcel_name VARCHAR NOT NULL,
                present_location VARCHAR NOT NULL,
                status VARCHAR NOT NULL,
                deliver_status VARCHAR NULL, 
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE ON UPDATE CASCADE)"""
        )

        for command in commands:
            self.cur.execute(command)
            print('tables created succesfully')

    def create_item(self, sql):
        self.cur.execute(sql)
        return {'message': 'Created succesfully'}, 201

    def check_item_exists(self, query):
        self.cur.execute(query)
        result = self.cur.fetchone()
        if result:
            return True
        return False

    def fetch_user(self, sql):
        self.cur.execute(sql)
        result = self.cur.fetchone()
        return result

    def drop_table(self, *table_names):
        '''Drops the tables created '''
        for table_name in table_names:
            drop_table = "DROP TABLE IF EXISTS {} CASCADE".format(table_name)
            print('all tables dropped')
            self.cur.execute(drop_table)