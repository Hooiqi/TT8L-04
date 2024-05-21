from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#mysql+mysqldb://<user>:<password>@<host>[:<port>]/<dbname>
#db = SQLAlchemy(app)

@app.route('/')
def create_event():
    return render_template('create_event.html')

if __name__ == "main":
    app.run(debug=True)
