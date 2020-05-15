from flask import Flask
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
api = Api(app)

db = SQLAlchemy(app)


class WineModel(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    vineyard = db.Column(db.String(80), nullable=False)

    @classmethod
    def get_wine_by_name(cls):
        pass


class Wine(Resource):
    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass


class WineList(Resource):
    def get(self):
        return WineModel.query.all()


api.add_resource(Wine, endpoint='wines/<int:id>')
api.add_resource(WineList, '/wines/')
