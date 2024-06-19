from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Admin, Membership
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user
from .forms import SignupForm
from flask_bcrypt import Bcrypt

auth = Blueprint('auth', __name__)
bcrypt = Bcrypt()

@auth.route('/update_admin_passwords')
def update_admin_passwords():
    admins = Admin.query.all()
    for admin in admins:
        try:
            # Attempt to check if the password is already hashed
            if not bcrypt.check_password_hash(admin.admin_pwd, 'dummy_password'):
                raise ValueError('Password is not hashed')
        except ValueError:
            # If a ValueError is raised, the password is not hashed, so we hash it
            admin.admin_pwd = bcrypt.generate_password_hash(admin.admin_pwd).decode('utf-8')
    db.session.commit()
    return "Admin passwords updated successfully."


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        id = request.form.get('id')
        password = request.form.get('password')

        user = User.query.filter_by(user_id=id).first()
        admin = Admin.query.filter_by(admin_id=id).first()

        if user:
            if user.user_pwd == password:
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        elif admin:
            if admin.admin_pwd == password:
                flash('Logged in successfully as Admin!', category='success')
                login_user(admin)
                return redirect(url_for('views.admin_home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("Loginpage.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    form = SignupForm()
    if request.method == 'POST':
        email = request.form.get('email')

        user = User.query.filter_by(user_email=email).first()

        if user:
            flash('Email already exists.', category='error')
        elif form.validate_on_submit():
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
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("Signuppage.html", user=current_user, form=form)  # Pass the 'form' variable to the template context

@auth.route('/update_member_status', methods=['POST'])
def update_member_status():
    if request.method == 'POST':
        for membership_id, status in request.form.items():
            if membership_id.startswith('status_'):
                membership_id = membership_id.split('_')[1]
                membership = Membership.query.get(membership_id)
                if membership:
                    membership.mstatus_name = status
                    db.session.commit()
                else:
                    flash(f'Membership with ID {membership_id} not found.', category='error')
        
        flash('Member statuses updated successfully!', category='success')
        return redirect(url_for('views.member_request'))  # Redirect to the member request page

    flash('Failed to update member statuses.', category='error')
    return redirect(url_for('views.member_request'))
