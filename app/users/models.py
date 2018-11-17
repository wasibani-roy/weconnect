from app.database import Database
import psycopg2
import os

db = Database(os.environ["DATABASE_URL"])


class User:
    """This class handles database transactions for the user"""

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def insert_user_data(self):
        try:
            query = "INSERT INTO users (username,password,email) VALUES(%s, %s,%s)"
            data = (self.username, self.password, self.email)
            user = db.cur.execute(query, data)
            print(user)
            return {'message': 'user registered succesfully'}, 201
        except Exception as e:
            raise e

    def fetch_user(self, username):
        try:
            query = "SELECT * FROM users WHERE username=%s"
            db.cur.execute(query, (username,))
            user = db.cur.fetchone()
            return user
        except Exception as e:
            return {'msg': 'user not found'}, 404

    def check_user(self, username):
        query = "SELECT * FROM users WHERE username=%s"
        db.cur.execute(query, (username,))
        user = db.cur.fetchone()
        if user:
            return True
        return False

    def fetch_all_users(self):
        """ Fetches all user records from the database"""
        try:
            query = ("SELECT * FROM users;")
            db.cur.execute(query)
            rows = db.cur.fetchall()
            return rows
        except (Exception, psycopg2.DatabaseError)as Error:
            raise Error

    @staticmethod
    def fetch_user_by_id(user_id):
        try:
            db = Database(os.environ["DATABASE_URL"])
            query = "SELECT * FROM users WHERE user_id=%s"
            db.cur.execute(query, (user_id,))
            user = db.cur.fetchone()
            print(user)
            return user
        except Exception as e:
            return {'msg': 'user not found'}, 404


