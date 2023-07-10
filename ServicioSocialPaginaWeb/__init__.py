# ServicioSocialPaginaWeb/__init__.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecret'

#####################################
#### DATABASE SETUP #################
#####################################

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://konosuba:konosuba@137.184.70.12/ssocial_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)


#####################################
#### LOGIN CONFIGS ##################
#####################################

login_manager = LoginManager()

login_manager.init_app(app)
login_manager.login_view = 'users.login'

#####################################

from ServicioSocialPaginaWeb.users.views import users
from ServicioSocialPaginaWeb.error_pages.handlers import error_pages
from ServicioSocialPaginaWeb.services.views import services
from ServicioSocialPaginaWeb.core.views import core
from ServicioSocialPaginaWeb.page_posts.views import news_posts

app.register_blueprint(core)
app.register_blueprint(services)
app.register_blueprint(error_pages)
app.register_blueprint(users)
app.register_blueprint(news_posts)
