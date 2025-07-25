from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////app/products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'a3f8e7b629d0c5f471a2b8d3c6e9f1021d4b5a7e9c8d3f0a1b2c4d5e6f7089'
db = SQLAlchemy(app)

from app import routes, models
