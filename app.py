from dotenv import load_dotenv
from flask import Flask, render_template, jsonify, request
import os
import db 
from werkzeug.security import check_password_hash, generate_password_hash
from db import get_db
load_dotenv()
app = Flask(__name__)
app.config['DATABASE'] =os.path.join(os.getcwd(),'flask.sqlite')
db.init_app(app)

@app.route('/')
def hello():
    title = "Georgina's Portfolio"
    return render_template("index.html", title=title)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/experience')
def experience():
    return render_template("experience.html")


@app.route('/projects')
def projects():
    return render_template("projects.html")


@app.route('/health')
def health():
    resp = jsonify(success=True)
    return resp

@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = f"User {username} is already registered."

        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return f"User {username} created successfully"
            return render_template("login.html")
        else:
            return error, 418

    ## TODO: Return a restister page
    return render_template("register.html")


@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            return render_template("about.html") 
        else:
            return error, 418
    
    ## TODO: Return a login page
    return render_template("login.html")



