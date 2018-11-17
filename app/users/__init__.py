from flask import Blueprint

from .views import Register, Login

users = Blueprint('users', __name__, url_prefix='/api/v2/auth')

users.add_url_rule('/signup', view_func=Register.as_view('register user'),
                    methods=['POST'], strict_slashes=False)
users.add_url_rule('/login', view_func=Login.as_view('login user'),
                    methods=['POST'], strict_slashes=False)

