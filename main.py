from cmath import exp
from flask import Flask, render_template, request, redirect, url_for,flash,session
from datetime import datetime

from flask_bcrypt import Bcrypt

from werkzeug.utils import secure_filename

import os

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore



cred = credentials.Certificate("firebase.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
ref = db.collection(u'users')

import pyrebase
firebaseConfig = {
  'apiKey': "AIzaSyDAxg_k_Ew_5GQpHb1TzVwkPKlbpMUwu6c",
  'authDomain': "assignment-task-3d9d1.firebaseapp.com",
  'projectId': "assignment-task-3d9d1",
  'storageBucket': "assignment-task-3d9d1.appspot.com",
  'messagingSenderId': "607993618252",
  'appId': "1:607993618252:web:5f988b115b775e7db1f9e9",
  'databaseURL': "https://assignment-task-3d9d1-default-rtdb.firebaseio.com/"
}

firebase_storage = pyrebase.initialize_app(firebaseConfig)
storage = firebase_storage.storage()

app = Flask(__name__)
app.secret_key = "asdfghjkl1234567890"
bcrypt = Bcrypt(app)
serverdate = datetime.now()
serverdate = serverdate.strftime("%d-%m-%Y,%H:%M:%S")

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            check = ref.document(username).get().to_dict()
            date = datetime.now()
            date = date.strftime("%d/%m/%Y %H:%M:%S")
            if check is None:
                ref.document(username).set({
                    u'username': username,
                    u'password': password,
                    u'email': email,
                    u'date_of_register': serverdate
                })
                flash('Registration Successful', 'success')
                return redirect(url_for('login'))

            else:
                flash("Username already exist", "danger")
                return redirect(url_for('register'))
        except Exception as e:
            print(e)
            flash("Server issue please try again later", "danger")
            return redirect(url_for('register'))
    if request.method == 'GET':
        return render_template('LoginPages/register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('LoginPages/login.html')

    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            check = ref.document(username).get().to_dict()
            if check:
                if check['username'] == username and check['password'] == password:
                    session.clear()
                    session["username"] = username
                    session["logged_in"] = True
                    flash("Login Success", "success")
                    return redirect(url_for('dashboard'))
                else:
                    flash("Invalid username or password", "danger")
                    return redirect(url_for('login'))
            else:
                flash("Username not found", "danger")
                return redirect(url_for('register'))
        except Exception as e:
            flash(f"Server issue please try again later {e}", "error")
            return redirect(url_for('login'))
# logout route
@app.route('/logout')
def logout():
    session.clear()
    flash("Logout Success", "success")
    return redirect(url_for('login'))


@app.route('/dashboard', methods=['GET'])
def dashboard():
    if request.method == 'GET':
        try:
            if 'username' in session:
                check = ref.document(session['username']).get().to_dict()
        
                if session['logged_in'] == True and check['username']==session['username']:
                    todos = ref.document(session['username']).collection('todo').get()
                    new_todos = []
                    for todo in todos:
                        new_todos.append(todo.to_dict())
                    return render_template('Dashboard/index.html', username=session['username'],todos=new_todos)
                else:
                    session.clear()
                    flash("Please login first", "error")
                    return redirect(url_for('login'))
            else:
                session.clear()
                flash("Please login first", "error")
                return redirect(url_for('login'))
        except Exception as e:
            session.clear()
            flash(f"Server issue please try again later {e}", "error")
            return redirect(url_for('login'))

# create todo 
@app.route('/todo/create', methods=['POST'])
def create_todo():
    if request.method == 'POST':
        try:
            if 'username' in session:
                check = ref.document(session['username']).get().to_dict()
                username = session['username']
                if session['logged_in'] == True and check['username']==session['username']:
                    title = request.form['title']
                    description = request.form['details']
                    expiry_date = request.form['expdate']
                    file = request.files['attachment']

                    date = datetime.now()
                    date = date.strftime("%d-%m-%Y,%H:%M:%S")
                    ref.document(session['username']).collection('todo').document(date).set({
                        u'title': title,
                        u'description': description,
                        u'date_created': date,
                        u'expiry_date': expiry_date
                    })
                    
                    if file:
                        try:
                            file.save(os.path.join('uploads/', secure_filename(file.filename)))
                            local_url_file = f'uploads/{file.filename}'
                            print(local_url_file)
                            ref.document(session['username']).collection('todo').document(date).update({
                                u'attachments': local_url_file
                            })
                            flash("Todo created successfully", "success")
                            return redirect(url_for('dashboard'))

                        except Exception as e:
                            print(e)
                            flash("File not uploaded", "danger")
                            return redirect(url_for('dashboard'))
                    
                    
                    flash("Todo created successfully", "success")
                    return redirect(url_for('dashboard'))
                else:
                    session.clear()
                    flash("Please login first", "error")
                    return redirect(url_for('login'))
            else:
                session.clear()
                flash("Please login first", "error")
                return redirect(url_for('login'))
        except Exception as e:
            flash(f"Server issue please try again later {e}", "error")
            return redirect(url_for('login'))


# delete todo
@app.route('/todo/delete', methods=['GET', 'POST'])
def delete_todo():
    if request.method == 'POST':
        try:
            if 'username' in session:
                check = ref.document(session['username']).get().to_dict()
                if session['logged_in'] == True and check['username']==session['username']:
                    todo_id = request.form['todo_id']
                    ref.document(session['username']).collection('todo').document(todo_id).delete()
                    flash("Todo deleted successfully", "success")
                    return redirect(url_for('dashboard'))
                else:
                    session.clear()
                    flash("Please login first", "error")
                    return redirect(url_for('login'))
            else:
                session.clear()
                flash("Please login first", "error")
                return redirect(url_for('login'))
        except Exception as e:
            flash(f"Server issue please try again later {e}", "error")
            return redirect(url_for('login'))

# update todo
@app.route('/todo/update', methods=['GET', 'POST'])
def update_todo():
    if request.method == 'POST':
        try:
            if 'username' in session:
                check = ref.document(session['username']).get().to_dict()
                if session['logged_in'] == True and check['username']==session['username']:
                    todo_id = request.form['todo_id']
                    title = request.form['title']
                    description = request.form['details']
                    expiry_date = request.form['expdate']
                    ref.document(session['username']).collection('todo').document(todo_id).update({
                        u'title': title,
                        u'description': description,
                        u'expiry_date': expiry_date
                    })
                    flash("Todo updated successfully", "success")
                    return redirect(url_for('dashboard'))
                else:
                    session.clear()
                    flash("Please login first", "error")
                    return redirect(url_for('login'))
            else:
                session.clear()
                flash("Please login first", "error")
                return redirect(url_for('login'))
        except Exception as e:
            flash(f"Server issue please try again later {e}", "error")
            return redirect(url_for('login'))
    


if __name__ == "__main__":
    app.run(debug=True)