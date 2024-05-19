from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
mysql+mysqldb://<user>:<password>@<host>[:<port>]/<dbname> #have not connected yet
db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "main":
    app.run(debug=True)
