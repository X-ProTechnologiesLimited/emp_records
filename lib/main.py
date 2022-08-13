from flask import Blueprint, render_template, request, redirect, flash, url_for
from . import db
from .email import send_email
from .token import generate_confirmation_token, confirm_token
from .forms import RegisterForm, PasswordReset, PasswordChange
from sqlalchemy import event
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user, login_user, login_manager
from . import records
from .models import User
import os, hashlib, os.path
path_to_script = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = '../templates'

main = Blueprint('main', __name__)

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@main.route('/shutdown')
def shutdown():
    shutdown_server()
    return 'Server shutting down...'


@event.listens_for(User.password, 'set', retval=True)
def hash_user_password(target, value, oldvalue, initiator):
    if value != oldvalue:
        return generate_password_hash(value)
    return value


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            password=form.password.data,
            name=form.name.data,
            dob=form.dob.data
        )

        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        new_user = User(email=form.email.data, name=form.name.data,
                        password=form.password.data, dob=form.dob.data,
                        attempt=0)

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()
        token = generate_confirmation_token(user.email)
        confirm_url = url_for('main.confirm_email', token=token, _external=True)
        html = render_template('activate.html', confirm_url=confirm_url)
        subject = "Please confirm your email"
        send_email(user.email, subject, html)
        flash('User registered. A confirmation email has been sent via email.', 'is-success')
        return redirect(url_for('auth.login'))

    return render_template('signup.html', form=form)


@main.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'is-danger')
    user = User.query.filter_by(email=email).first_or_404()
    if user.is_verified:
        flash('Account already confirmed. Please login.', 'is-warning')
        return redirect(url_for('auth.login'))
    else:
        user.is_verified = True
        db.session.add(user)
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'is-success')

    login_user(user)
    return redirect(url_for('main.portal'))


@main.route('/request/reset_password', methods=['GET', 'POST'])
def password_reset():
    form = PasswordReset(request.form)
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            dob=form.dob.data,
        )

        token = generate_confirmation_token(user.email)
        password_reset_url = url_for('main.password_confirm', token=token, _external=True)
        html = render_template('reset_request.html', password_reset_url=password_reset_url)
        subject = "Your link to reset your password"
        send_email(user.email, subject, html)
        flash('The link for password reset has been sent via email.', 'is-success')
        return redirect(url_for('auth.login'))

    return render_template('password_reset_request.html', form=form)


@main.route('/change/password/<token>', methods=['GET', 'POST'])
# @login_required
def password_confirm(token):
    form = PasswordChange(request.form)
    if form.validate_on_submit():
        try:
            email = confirm_token(token)
            user = User.query.filter_by(email=email).first_or_404()
            if user.is_verified:
                user.password = form.password.data
                user.attempt = 0
                user.is_locked = False
                db.session.add(user)
                db.session.commit()
                flash('Password changed successfully.', 'is-success')
                return redirect(url_for('auth.login'))
            else:
                flash('You have not confirmed your account. Please activate your account first!', 'is-danger')
                return redirect(url_for('auth.login'))
        except:
            flash('The confirmation link is invalid or has expired.', 'is-danger')
            return redirect(url_for('auth.login'))

    return render_template('password_reset_confirm.html', form=form)

@main.route('/portal')
@login_required
def portal():
    return render_template('portal.html', name=current_user.name)


@main.route('/employees')
def get_emp_records():
    """
    :author: Krishnendu Banerjee.
    :date: 29/11/2019.
    :description: Function that calls to API to search all assets on the database
    :access: public
    :method: post
    :return: post: module: search; function: search_all_packages
    """
    return records.get_emp_records()


@main.route('/get_emp_details/<id>', methods=['GET'])
def get_emp_details(id):
    return records.get_emp_data(id)


@main.route('/employee/search', methods=['GET','POST'])
def search_emp_record():
    if request.method == 'POST':
        field = request.form.get('Field')
        if 'Date' in field:
            return records.search_emp_record(field, request.form.get('date'))
        else:
            return records.search_emp_record(field, request.form.get('keyword'))
    else:
        return render_template('search_employee.html', title='Search Employee', action='/employee/search')
