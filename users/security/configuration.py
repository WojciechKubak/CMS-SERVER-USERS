from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

# Initializing JWTManager for handling JSON Web Tokens in Flask.
jwt_manager = JWTManager()
# Flask-Bcrypt is initialized to handle password hashing and verification.
bcrypt = Bcrypt()
