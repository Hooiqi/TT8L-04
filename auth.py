from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import User, Admin, db
from flask_login import login_user, login_required, logout_user, current_user
from forms import SignupForm
from flask_bcrypt import Bcrypt

auth = Blueprint('auth', __name__)
bcrypt = Bcrypt()

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.user_pwd.data).decode('utf-8')
        new_user = User(
            user_id=form.user_id.data,
            user_name=form.user_name.data,
            user_email=form.user_email.data,
            user_phone=form.user_phone.data,
            user_pwd=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()

        flash(f'User created successfully!', 'success')
        return redirect(url_for('auth.login'))
    
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {getattr(form, field).label.text}: {error}", 'danger')

    return render_template('Signuppage.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        id = request.form.get('id')
        password = request.form.get('password')

        user = User.query.filter_by(user_id=id).first()
        admin = Admin.query.filter_by(admin_id=id).first()

        if user:
            if bcrypt.check_password_hash(user.user_pwd, password):
                login_user(user, remember=True)
                return redirect(url_for('user_view.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        elif admin:
            if admin.admin_pwd == password:
                login_user(admin)
                return redirect(url_for('admin_view.admin_home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('ID does not exist.', category='error')

    return render_template("Loginpage.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html", user=current_user)