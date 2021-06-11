from dotenv import load_dotenv
from flask import Flask, render_template

load_dotenv()
app = Flask(__name__)

@app.route('/')
def hello():
    title = "Name's Portfolio"
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

