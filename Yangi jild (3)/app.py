# save this as app.py
from flask import Flask, render_template, request, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = "kalit"
app.permanent_session_lifetime = 3600


conn = sqlite3.connect("base.db")
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        login TEXT UNIQUE, 
        password TEXT, 
        name TEXT, 
        age INTEGER)''')

conn.commit()
conn.close()

@app.route("/")
def home():
    conn = sqlite3.connect("base.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    users = c.fetchall()
    conn.close()
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("index.html", users=users)


@app.route("/add", methods=["POST", "GET"])
def add_user():
    if "user" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        login = request.form["login"]
        password = request.form["password"]
        name = request.form["name"]
        age = request.form["age"]

        conn = sqlite3.Connection("base.db")
        c = conn.cursor()
        
        c.execute("SELECT * FROM users WHERE login = ?", (login,))
        existing_user = c.fetchone()
        if existing_user:
            return "User with this login already exists"
        else:
            c.execute("INSERT INTO users (login, password, name, age) VALUES (?, ?, ?, ?)",
                  (login, password, name, age))
            conn.commit()
            conn.close()
            return redirect(url_for("home"))
        

    return render_template("user.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        login = request.form["login"]
        password = request.form["password"]

        conn = sqlite3.connect("base.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE login = ? AND password = ?", (login, password))
        user = c.fetchone()
        conn.close()

        if user:
            session["user"] = user[1]
            return redirect(url_for("home"))
        else:
            return "Invalid credentials"

    if "user" in session:
        return redirect(url_for("home"))
    
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)