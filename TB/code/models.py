from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    city_name = db.Column(db.String(80))
    state = db.Column(db.String(80))
    country = db.Column(db.String(80))
    coords = db.Column(db.String(80))
    degree_unit = db.Column(db.String(80))

    def __repr__(self):
        return f'<User user_id={self.user_id} city_name={self.city_name}>'
