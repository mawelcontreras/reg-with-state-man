from os import path
from sqlite3 import dbapi2
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
DB_name = "database.db"

def create_app():
    app = Flask(__name__)

    #encryption
    app.config['SECRET_KEY'] = 'asdasd'
    
    #database init
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_name}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    #registering blueprints
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Steps

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('Website/' + DB_name):
        db.create_all(app=app)
        print('Database Created!')