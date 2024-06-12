from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_bcrypt import Bcrypt
from forms import EventForm
from models import *


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:Ghq1003.@localhost/event_management_system'
app.config['SECRET_KEY'] = 'ihopethiscanrun'
db.init_app(app)
csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)


@app.route('/')
def events():
    events = Event.query.all()
    return render_template('Homepage.html', events=events)

if __name__ == "__main__":
    app.run(debug=True)

