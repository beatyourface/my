# -*- coding: utf-8 -*-
"""
Created on Wed Apr  9 07:36:25 2025

@author: Administrator
"""
from flask_bootstrap import Bootstrap4
from flask_ckeditor import CKEditor
from flask_login import LoginManager
# from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_debugtoolbar import DebugToolbarExtension
#from flask_migrate import Migrate


bootstrap = Bootstrap4()
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
ckeditor = CKEditor()
# mail = Mail()
moment = Moment()
toolbar = DebugToolbarExtension()
#migrate = Migrate()


@login_manager.user_loader
def load_user(user_id):
    from hyyb.models import Admin
    user = Admin.query.get(int(user_id))
    return user


login_manager.login_view = 'auth.login'
# login_manager.login_message = 'Your custom message'
login_manager.login_message_category = 'warning'
