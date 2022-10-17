from flask import Flask, request, jsonify

import pymongo


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
        data = request.get_json()
        # afret login we will add user_id in session
        # here data is a dictionary which should contain todo title, description, status, due_date of todo item and finally user_id
        print(data)
        try:
            db.users.data['user_id'].todo.insert_one({
                'title': data['title'],
                'description': data['description'],
                'status': data['status'],
                'due_date': data['due_date'],
            })
            return jsonify({"message": "Todo added"}), 200
        except Exception as e:
            return jsonify({"message": e})

# api for update todo
@app.route('/todo/update', methods=['PUT'])
def update_todo():
    if request.method == 'PUT':
        data = request.get_json()
        # afret login we will add user_id in session
        # here data is a dictionary which should contain todo title, description, status, due_date of todo item and finally user_id
        print(data)
        try:
            db.users.data['user_id'].todo.update_one({
                'title': data['title'],
                'description': data['description'],
                'status': data['status'],
                'due_date': data['due_date'],
            })
            return jsonify({"message": "Todo updated"}), 200
        except Exception as e:
            return jsonify({"message": e})

# api for delete todo
@app.route('/todo/delete', methods=['DELETE'])
def delete_todo():
    if request.method == 'DELETE':
        data = request.get_json()
        print(data)
        # afret login we will add user_id in session
        # here data is a dictionary which should contain todo title, description, status, due_date of todo item and finally user_id
        try:
            db.users.data['user_id'].todo.delete_one({
                'title': data['title'],
                'description': data['description'],
                'status': data['status'],
                'due_date': data['due_date'],
            })
            return jsonify({"message": "Todo deleted"}), 200
        except Exception as e:
            return jsonify({"message": e})

# api for delete all todos
@app.route('/todo/delete/all', methods=['DELETE'])
def delete_all_todos():
    if request.method == 'DELETE':
        # afret login we will add user_id in session
        # here we need to have user_id first to get all todos for that user
        # other wise it will delete all todos for all users
        # this will create confusion
        # it will be a good idea to have user_id in session
        # suppose we have user_id in session
        # and data['user_id'] is the user_id in session
        try:
            db.users.data['user_id'].delete_many({})
            return jsonify({"message": "All todos deleted"}), 200
        except Exception as e:
            return jsonify({"message": e})

# api for get all todos
@app.route('/todo/get', methods=['GET'])
def get_all_todos():
    if request.method == 'GET':
        # afret login we will add user_id in session
        # here we need to have user_id first to get all todos for that user
        # other wise we can get all todos for all users
        # it will be a good idea to have user_id in session
        # suppose we have user_id in session
        # and data['user_id'] is the user_id in session
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
        # todo id is the id of todo item
        # while adding todo todo id will be generated automatically
        # we have to pass todo id in url
        # also with that we need to have user_id in session

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
        data = request.get_json()
        print(data)
        try:
            server_data = db.users.find_one({"name": data['name']})
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
        data = request.get_json()
        print(data)
        try:
            server_data = db.users.find_one({"name": data['name']})
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
        # this api should be used only by admin
        # so we need to check if user is admin or not
        # if user is admin then only we will return all users
        try:
            data = db.users.find()
            users = []
            for i in data:
                users.append(i)
            return jsonify({"message": "Users fetched", "users": users}), 200
        except Exception as e:
            return jsonify({"message": e})



if __name__ == "__main__":
    app.secret_key = "govind"
    app.debug = True
    app.run()
