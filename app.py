from flask import Flask, jsonify, request
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from db import db
from resources.item import blp as ItemBlueprint

app = Flask(__name__)

# Налаштування бази даних
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# Налаштування JWT
app.config["JWT_SECRET_KEY"] = "super_secret_key"
jwt = JWTManager(app)

# JWT обробка помилок
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({"message": "Token expired", "error": "token_expired"}), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({"message": "Invalid token", "error": "invalid_token"}), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({"message": "Token missing", "error": "authorization_required"}), 401

# Ініціалізація API
api = Api(app)
api.register_blueprint(ItemBlueprint)

# Ендпоінти для аутентифікації
@api.route("/login")
class LoginResource:
    def post(self):
        data = request.get_json()
        if data["username"] == "admin" and data["password"] == "password":
            access_token = jwt.create_access_token(identity="admin")
            return {"access_token": access_token}, 200
        return {"message": "Invalid credentials"}, 401

@api.route("/logout")
class LogoutResource:
    def post(self):
        return {"message": "Logout successful"}, 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)
