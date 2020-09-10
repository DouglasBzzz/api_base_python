from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps

database_connect = create_engine('sqlite:///exemplo.db')
app = Flask(__name__)
api = Api(app)

class Users(Resource):
    def get(self):
        conn = database_connect.connect()
        query = conn.execute("select * from user")
        result = [dict(zip(tuple(query.keys()),i)) for i in query.cursor]
        return jsonify(result)

    def post(self):
        conn = database_connect.connect()
        nome = request.json['name']
        e_mail = request.json['email']

        conn.execute(
            f"insert into user(id, name, email) values(null, '{nome}', '{e_mail}')"
        )

        query = conn.execute("select * from user order by id desc limit 1")
        result = [dict(zip(tuple(query.keys()),i)) for i in query.cursor]
        return jsonify(result)

    def put(self):
        conn = database_connect.connect()
        id = request.json['id']
        nome = request.json['name']
        e_mail = request.json['email']

        conn.execute(f"update user set name = '{nome}', email = '{e_mail}'"
                     f"where id = {int(id)}")

        query = conn.execute(f"select * from user where id = {int(id)}")
        result = [dict(zip(tuple(query.keys()),i)) for i in query.cursor]
        return jsonify(result)


class UserById(Resource):
    def delete(self,id):
        conn = database_connect.connect()
        conn.execute(f"delete from user where id = {int(id)}")
        return {"status":"sucesso"}

    def get(self, id):
        conn = database_connect.connect()
        query = conn.execute(f"select * from user where id = {int(id)}")
        result = [dict(zip(tuple(query.key()), i)) for i in query.cursor]
        return jsonify(result)

api.add_resource(Users, '/users')
api.add_resource(UserById, '/users/<id>')

if __name__ == '__main__':
    app.run()