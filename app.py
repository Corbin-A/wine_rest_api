from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
api = Api(app)

db = SQLAlchemy(app)

@app.route('/')
def index():
    return 'test'


class WineModel(db.Model):
    __tablename__ = 'wine'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    vineyard = db.Column(db.String(80), nullable=False)

    def __init__(self, name, vineyard):
        self.name = name
        self.vineyard = vineyard

    def json(self):
        return {'id': self.id, 'name': self.name, 'vineyard': self.vineyard}

    @classmethod
    def get_wine_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def remove_from_db(self):
        db.session.delete(self)
        db.session.commit()


class Wine(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str)
    parser.add_argument('vineyard', type=str)

    def get(self, id):
        return WineModel.get_wine_by_id(id).json()

    def post(self):
        pass

    def put(self, id):
        wine = WineModel.get_wine_by_id(id)
        if wine is None:
            return {'message': 'Wine not found'}, 404

        data = Wine.parser.parse_args()
        wine.name = data['name']
        wine.vineyard = data['vineyard']

        wine.save_to_db()

        return wine.json(), 200

    def delete(self, id):
        wine = WineModel.get_wine_by_id(id)
        wine.remove_from_db()
        return {'message': 'Wine Deleted'}, 200


class WineList(Resource):
    def get(self):
        return {'wines': [result.json() for result in WineModel.query.all()]}

    def post(self):
        data = Wine.parser.parse_args()

        wine = WineModel(data['name'], data['vineyard'])

        wine.save_to_db()

        return wine.json(), 201


db.create_all()
api.add_resource(Wine, '/wines/<int:id>')
api.add_resource(WineList, '/wines/')
