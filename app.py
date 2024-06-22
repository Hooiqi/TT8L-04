from flask import Flask
from flask_wtf import CSRFProtect
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from models import db
import stripe

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://<user>:<password>@<host>[:<port>]/<dbname>'
app.config['SECRET_KEY'] = '\xfcQz\x82\x00\xb5\xee\x14\x15\x8b\x8c\xbd\x1cSbP\xaa\x04k\x92\x9e\x15\xdf\xa6'
app.config['UPLOAD_FOLDER'] = 'static/images/'

# Initialize extensions
db.init_app(app)
csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

# Stripe configuration
app.config['STRIPE_SECRET_KEY'] = 'sk_test_51PMWarFeLdpgIRLCcD1YhpdSwJESnWBcMmxvtFXvlx9aEfh11QwoCY3eaSMi43B7Ho1BBIld9qMDAaCRIsVbUZpw00lInyAKH0'
stripe.api_key = app.config['STRIPE_SECRET_KEY']

@login_manager.user_loader
def load_user(user_id):
    from models import Admin, User
    return Admin.query.get(user_id) or User.query.get(user_id)

# Import and register blueprints
from auth import auth
from user_view import user_view
from admin_view import admin_view

app.register_blueprint(auth, url_prefix='/')
app.register_blueprint(user_view, url_prefix='/')
app.register_blueprint(admin_view, url_prefix='/admin')

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
