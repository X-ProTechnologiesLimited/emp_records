from flask import Flask, render_template, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, current_user
from flask_admin import Admin
from flask_mail import Mail
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from datetime import timedelta


TEMPLATE_DIR = '../templates'

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
mail = Mail()

def create_app():
    app = Flask(__name__, template_folder=TEMPLATE_DIR)

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)
    app.config['SESSION_REFRESH_EACH_REQUEST'] = True
    app.config['SECURITY_PASSWORD_SALT'] = 'my_precious_two'
    app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = 'xprotech.contact@gmail.com'
    app.config['MAIL_PASSWORD'] = 'fwgvkonzuriefrrv'

    from .models import User, Emp_main

    with app.app_context():
        db.init_app(app)
        mail.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = "User needs to be logged in to view this page"
    login_manager.login_message_category = "is-info"
    login_manager.init_app(app)

    class MyModelView(ModelView):
        column_searchable_list = ('name', 'email',)
        column_list = ('name', 'email', 'dob', 'is_admin', 'is_verified', 'is_locked', 'attempt')
        column_default_sort = 'name'
        column_filters = ('name', 'email')
        column_editable_list = ('is_admin', 'is_verified', 'is_locked')
        form_create_rules = ('email', 'name', 'password', 'dob', 'is_admin',
                             'is_verified', 'attempt', 'is_locked')
        form_edit_rules = ('email', 'name', 'dob', 'is_admin', 'is_verified', 'is_locked')

        def is_accessible(self):
            if current_user.is_authenticated and current_user.is_admin is True:
                return current_user.is_authenticated
            else:
                return abort(403)
        def not_auth(self):
            return 'You are not allowed to use the dashboard'

    class Logout(BaseView):
        @expose('/')
        def logout(self):
            return redirect(url_for('auth.logout'))

    class Portal(BaseView):
        @expose('/')
        def portal(self):
            return redirect(url_for('main.portal'))

    admin = Admin(app, name='User Management')
    admin.add_view(MyModelView(User, db.session))
    admin.add_view(Portal(name='Portal', endpoint='portal'))
    admin.add_view(Logout(name='Logout', endpoint='logout'))

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
