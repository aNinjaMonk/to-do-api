from math import dist
from flask import Flask, request, jsonify

import pymongo

import json

# you cannot use my username and password
# i have restricted access to my database from outside my network
# you will have to create your own database and use your own username and password
# you can use the same database name and collection name

mongoUser = "root"
mongoPass = "govind12"
client = pymongo.MongoClient(f"mongodb+srv://{mongoUser}:{mongoPass}@todo-api-assessment-dat.8aeftkc.mongodb.net/test")
db = client.todo_db

app = Flask(__name__)



# api for add todo
@app.route('/todo/create', methods=['POST'])
def add_todo():
    if request.method == 'POST':
        data = {
            "title": request.form['title'],
            "description": request.form['description'],
            "status": request.form['status'],
            "due_date": request.form['due_date'],
            "username": request.form['username']
        }
        try:
            db.todo.insert_one(data)
            return jsonify({"message": "Todo added successfully"})
        except Exception as e:
            print(e)
            return jsonify({"message": "todo not added"})

# api for update todo
@app.route('/todo/update', methods=['PUT'])
def update_todo():
    if request.method == 'PUT':
        data = {
            "title": request.form['title'],
            "description": request.form['description'],
            "status": request.form['status'],
            "due_date": request.form['due_date'],
            "username": request.form['username']
        }
        print(data)
        try:
            db.todo.update_one({"username": data['username']}, {"$set": data})
            db.todo.update_one({
                'title': data['title'],
                'description': data['description'],
                'status': data['status'],
                'due_date': data['due_date'],
                'username': data['username']
            })
            return jsonify({"message": "Todo updated"}), 200
        except Exception as e:
            return jsonify({"message": e})

# api for delete todo
@app.route('/todo/delete', methods=['DELETE'])
def delete_todo():
    if request.method == 'DELETE':
        data = {
            "title": request.form['title'],
            "description": request.form['description'],
            "status": request.form['status'],
            "due_date": request.form['due_date'],
            "username": request.form['username']
        }
        try:
            db.users.todo.delete_one({"username": data['username']})
            return jsonify({"message": "Todo deleted"}), 200
        except Exception as e:
            return jsonify({"message": e})

# api for delete all todos
@app.route('/todo/delete/all', methods=['DELETE'])
def delete_all_todos():

    if request.method == 'DELETE':
        data = {
            "username": request.form['username']
        }
        try:
            db.users.todo.delete_many({"username": data['username']})
            return jsonify({"message": "All todos deleted"}), 200
        except Exception as e:
            return jsonify({"message": e})

# api for get all todos
@app.route('/todo/get', methods=['GET'])
def get_all_todos():
    if request.method == 'GET':
        try:
            data = db.users.data['user_id'].find()
            todos = []
            for i in data:
                todos.append(i)
            return jsonify({"message": "Todos fetched", "todos": todos}), 200
        except Exception as e:
            return jsonify({"message": e})

# api for get a todo
@app.route('/todo/get/<id>', methods=['GET'])
def get_a_todo(id):
    if request.method == 'GET':
        try:
            data = db.users.data['user_id'].todo.find_one({"_id": id})
            if data is None:
                return jsonify({"message": "Todo not found"}), 404
            else:
                return jsonify({"message": "Todo fetched", "todo": data}), 200
        except Exception as e:
            return jsonify({"message": e})

# api for register
@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        data = {
            'username': request.form['username'],
            'password': request.form['password'],
            'email': request.form['email']
        }
        print(data)
        try:
            server_data = db.users.find_one({"name": data['username']})
            if server_data is None:
                db.users.insert_one(data)
                return jsonify({"message": "User registered"}), 200
            else:
                return jsonify({"message": "User already exists"}), 409
        except Exception as e:
            return jsonify({"message": e})


# api for login
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = {
            'username': request.form['username'],
            'password': request.form['password']
        }
        print(data)
        try:
            server_data = db.users.find_one({"username": data['username']})
            if server_data is None:
                return jsonify({"message": "User not found"}), 404
            else:
                if server_data['password'] == data['password']:
                    return jsonify({"message": "Login successful"}), 200
                else:
                    return jsonify({"message": "Wrong password"}), 401
        except Exception as e:
            return jsonify({"message": e})

#api to get all users
@app.route('/users', methods=['GET'])
def get_all_users():
    if request.method == 'GET':
        try:
            data = db.users.find()
            data = str(list(data))
            return jsonify({"users": data}), 200
        except Exception as e:
            return jsonify({"message": e})



if __name__ == "__main__":
    app.secret_key = "govind"
    app.debug = True
    app.run()