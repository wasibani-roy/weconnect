from flask import jsonify, make_response, request
from .models import User
import flask.views
from werkzeug.security import check_password_hash, generate_password_hash
import psycopg2
from flask_jwt_extended import ( create_access_token)


class Register(flask.views.MethodView):
    def get(self):
        try:
            use = User('username', 'password')
            rows = use.fetch_all_users()
            if rows == True:
                return {"msg": " There are no users at the momnet"}, 200
            return make_response(jsonify({"users": rows}), 200)
        except (Exception, psycopg2.DatabaseError)as Error:
            print(Error)

    def post(self):
        try:
            parser = request.get_json()
            username = parser.get('username')
            user_password = parser.get('password')
            email = parser.get('email')
            password = generate_password_hash(
                user_password, method='sha256')


            """creating an insatnce of the user class"""
            use = User(username, email, password)
            user = use.check_user(username)
            if user:
                return make_response(jsonify({'message': 'Username already exists'}), 403)
            use.insert_user_data()
            return make_response(jsonify({'message': "you have succesfully signed up"}), 201)
        except Exception as e:
            raise e


class Login(flask.views.MethodView):
    def post(self):
        """
        Allows users to login to their accounts

        """
        data = request.get_json()
        username = data['username']
        password = data['password']
        existing_user = User(username=username, email="none", password=password)


        """
            read from database to find the user and then check the password

        """

        user = existing_user.fetch_user(username)
        # print(user)
        if user and check_password_hash(user['password'], password):
            print(user)
            print(type(user))
            access_token = create_access_token(identity={"user_id":user['user_id'], "username":user['username']})
            return make_response(jsonify({
                    "message": "You have successfully logged in {}".format(user['username']), "access token": access_token}), 200)
        else:
            return {'message': 'Invalid credentials'}, 401
