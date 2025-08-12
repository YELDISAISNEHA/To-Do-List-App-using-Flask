from bson.objectid import ObjectId
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from pymongo import MongoClient
import secrets

app = Flask(__name__)

app.secret_key = secrets.token_hex(16)

client = MongoClient("mongodb://localhost:27017/")
db = client.to_do_users
collection = db.users

@app.route('/', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        user = collection.find_one({"email": email, "password": password})

        if user:
            session["fullname"] = user.get("fullname")
            session["email"] = user.get("email")
            return redirect(url_for('tasks_page'))
        else:
            flash("Invalid email or password")
            return redirect(url_for('register'))
    return render_template('index.html')

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["fullname"]
        email = request.form["email"]
        password = request.form["password"]

        collection.insert_one({
            "fullname": name,
            "email": email,
            "password": password
        })
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/tasks_page')
def tasks_page():
    fullname = session.get("fullname")
    email = session.get("email")
    tasks = []
    if email:
        tasks = list(db.tasks.find({"email": email}))
    return render_template('tasks_page.html', name=fullname, email=email, tasks=tasks)

@app.route('/add_task', methods=["POST"])
def add_task():
    task = request.form.get("task")
    email = session.get("email")
    if email:
        db.tasks.insert_one({
            "email": session["email"],
            "task": task
        })
    return redirect(url_for('tasks_page'))

@app.route('/delete_task/<task_id>', methods=["DELETE"])
def delete_task(task_id):
    result = db.tasks.delete_one({"_id": ObjectId(task_id)})
    if result.deleted_count > 0:
        return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)