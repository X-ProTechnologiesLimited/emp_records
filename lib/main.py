from flask import Blueprint, render_template, request, redirect, flash, url_for, abort
from . import db
from .email import send_email
from .token import generate_confirmation_token, confirm_token
from .forms import RegisterForm, PasswordReset, PasswordChange
from sqlalchemy import event
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user, login_user, login_manager
from . import records
from .models import User, Emp_contact, Emp_main
import os.path
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
    return redirect(url_for('auth.login'))


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
    return redirect(url_for('auth.modify_password'))


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
    if current_user.is_admin:
        return render_template('portal.html', name=current_user.name)
    else:
        return render_template('emp_portal.html', name=current_user.name)


@main.route('/employees')
@login_required
def get_emp_records():
    """
    :author: Krishnendu Banerjee.
    :date: 29/11/2019.
    :description: Function that calls to API to search all assets on the database
    :access: public
    :method: post
    :return: post: module: search; function: search_all_packages
    """
    if current_user.is_admin:
        return records.get_emp_records('admin')
    else:
        return records.get_emp_records('employee')


@main.route('/my_employees')
@login_required
def my_emp_records():
    """
    :author: Krishnendu Banerjee.
    :date: 29/11/2019.
    :description: Function that calls to API to search all assets on the database
    :access: public
    :method: post
    :return: post: module: search; function: search_all_packages
    """
    user_id = current_user.id
    user = User.query.filter_by(id=user_id).first()
    emp_contact = Emp_contact.query.filter_by(email=user.email).first()
    employee = Emp_main.query.filter_by(id=emp_contact.id).first()

    fullname = f'{employee.firstname} {employee.lastname}'
    return records.get_emp_records('manager', manager_name=fullname)

@main.route('/get_emp_details/<id>', methods=['GET'])
@login_required
def get_emp_details(id):
    if current_user.is_admin:
        return records.get_emp_data(id, 'admin')
    else:
        return abort(403)


@main.route('/my_emp_details/<id>', methods=['GET'])
@login_required
def my_emp_details(id):
    if records.verify_manager(id, current_user.id):
        return records.get_emp_data(id, 'employee')
    else:
        return abort(403)

@main.route('/employee/search', methods=['GET','POST'])
@login_required
def search_emp_record():
    if current_user.is_admin:
        if request.method == 'POST':
            field = request.form.get('Field')
            if 'Date' in field:
                return records.search_emp_record(field, request.form.get('date'))
            else:
                return records.search_emp_record(field, request.form.get('keyword'))
        else:
            return render_template('search_employee.html', title='Search Employee', action='/employee/search')

    else:
        return abort(403)
