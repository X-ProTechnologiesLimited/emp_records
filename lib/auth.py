from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .models import User, Emp_contact, Emp_main
from .nocache import nocache
from .forms import SelfPasswordChange
import os.path
from . import records
from . import db
path_to_script = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = '../templates'

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user: # or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.', 'is-danger')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

    if user.attempt >= 4:
        user.is_locked = True
        db.session.add(user)
        db.session.commit()
        flash('You have locked your account.', 'is-danger')
        return redirect(url_for('auth.login'))

    if not check_password_hash(user.password, password):
        user.attempt = user.attempt + 1
        db.session.add(user)
        db.session.commit()
        flash('Incorrect Password. Please try again', 'is-danger')
        return redirect(url_for('auth.login'))

    # if the above check passes, then we know the user has the right credentials

    if user.is_verified and not user.is_locked:
        login_user(user, remember=remember)
        user.attempt = 0
        db.session.add(user)
        db.session.commit()
        if user.is_admin:
            return redirect('/admin')
        else:
            return redirect(url_for('main.portal'))
    else:
        flash('Your user is not enabled. Please contact your HR Admin.', 'is-warning')
        return redirect(url_for('auth.login'))

@auth.route('/employee/new', methods=['GET', 'POST'])
@login_required
def create_emp_record():
    """
        :author: Krishnendu Banerjee.
        :date: 29/11/2019.
        :description: Function that calls to API to search all assets on the database
        :access: public
        :method: post
        :return: post: module: search; function: search_all_packages
        """
    if not current_user.is_admin:
        return abort(403)
    if request.method == 'POST':
        if records.create_emp_record() == False:
            flash('Employee Not Created. \n'
                  'A duplicate email record found')
            return redirect(url_for('auth.create_emp_record'))
        else:
            return redirect(url_for('main.get_emp_records'))
    else:
        emp_list = Emp_main.query.all()
        return render_template('emp_create.html', emp_list=emp_list)


@auth.route('/profile')
@login_required
def get_self_profile():
    user_id = current_user.id
    user = User.query.filter_by(id=user_id).first()
    employee = Emp_contact.query.filter_by(email=user.email).first()
    return records.get_emp_data(employee.id, 'employee')



@auth.route('/employee/update', methods=['POST'])
@login_required
def update_emp_record():
    id = request.form.get('Id')
    user = User.query.filter_by(id=current_user.id).first()
    employee = Emp_contact.query.filter_by(email=user.email).first()
    if not current_user.is_admin:
        if not records.verify_manager(int(id), current_user.id):
            if int(id) != employee.id:
                return abort(403)

    if current_user.is_admin or records.verify_manager(int(id), current_user.id):
        role = 'admin'
    else:
        role = 'employee'

    if request.method == 'POST':
        if records.update_emp_record(id, role) != True:
            flash('Employee is not updated. \n'
                  'A duplicate email record found')
            return records.get_emp_data(id, role)
        else:
            return records.get_emp_data(id, role)
    else:
        return render_template('emp_info.html', title='Update Employee', action='/employee/update')


@auth.route('/employee/<action>/<id>', methods=['GET', 'POST'])
@login_required
def get_form_employee(id, action):
    emp_profile = records.get_emp_profile(id)
    emp_contact = records.get_emp_contact(id)
    emp_bank = records.get_emp_bank(id)
    emp_name = records.get_emp_name(id)
    user_id = current_user.id
    user = User.query.filter_by(id=user_id).first()
    employee = Emp_contact.query.filter_by(email=user.email).first()
    if not current_user.is_admin:
        if not records.verify_manager(int(id), current_user.id):
            if int(id) != employee.id:
                return abort(403)

    if action == 'update':
        emp_list = Emp_main.query.all()
        return render_template('emp_details.html',
                               Id=emp_profile.id,
                               per_title=emp_profile.per_title,
                               firstname=emp_profile.firstname,
                               lastname=emp_profile.lastname,
                               title=emp_profile.title,
                               type=emp_profile.type,
                               status=emp_profile.status,
                               manager=emp_profile.manager,
                               dob=emp_profile.dob,
                               doj=emp_profile.doj,
                               dol=emp_profile.dol,
                               salary=emp_profile.salary,
                               address=emp_contact.address,
                               phone=emp_contact.phone,
                               mobile=emp_contact.mobile,
                               email=emp_contact.email,
                               bank=emp_bank.bank,
                               sortcode=emp_bank.sortcode,
                               account=emp_bank.account,
                               emp_list=emp_list)

    elif action == 'delete' and current_user.is_admin:
        return render_template('delete_emp.html', Id=emp_profile.id, Employee_Name=emp_name,
                               title='Delete Employee', action='/employee/delete')
    else:
        return abort(403)


@auth.route('/employee/delete', methods=['GET', 'POST'])
@nocache
@login_required
def delete_emp_record():
    """
    :author: Krishnendu Banerjee.
    :date: 29/11/2019.
    :description: Function that calls to API to search all assets on the database
    :access: public
    :method: post
    :return: post: module: search; function: search_all_packages
    """
    id = request.form.get('Id')
    if request.method == 'POST':
        return records.delete_emp_record(id)
    else:
        return render_template('emp_info.html', title='Delete Employee', action='/employee/delete')



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/change_password', methods=['GET', 'POST'])
@login_required
def modify_password():
    form = SelfPasswordChange(request.form)
    if form.validate_on_submit():
        current_password = form.curr_password.data
        new_pasword = form.password.data
        user_id = current_user.id
        user = User.query.filter_by(id=user_id).first()
        if not check_password_hash(user.password, current_password):
            flash('The current password doesnt match our records.', 'is-danger')
            return redirect(url_for('auth.modify_password'))
        else:
            user.password = new_pasword
            db.session.add(user)
            db.session.commit()
            flash('Password modified successfully.', 'is-success')
            return render_template('message_banner.html', title='')

    return render_template('self_modify_password.html', form=form)



