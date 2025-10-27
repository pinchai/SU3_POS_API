from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from datetime import timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

# --- JWT config ---
app.config["JWT_SECRET_KEY"] = "change-me"  # put in ENV in production
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)

jwt = JWTManager(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)


# model
import model


# routes
import routes


if __name__ == '__main__':
    app.run()
