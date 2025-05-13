# -*- coding: utf-8 -*-
"""
Created on Fri Apr 11 07:04:58 2025

@author: Administrator
"""
from flask import render_template, flash, redirect, url_for, Blueprint
from flask_login import login_user, logout_user, login_required, current_user

from hyyb.forms import LoginForm
from hyyb.models import Admin
from hyyb.utils import redirect_back

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('message.index'))   #S

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        admin = Admin.query.filter(Admin.username == username).first()
        if admin:
            if username == admin.username and admin.validate_password(password):
                login_user(admin, remember)
                flash('Welcome back.'+current_user.username, 'info')
                return redirect_back()
            flash('Invalid username or password.', 'warning')
        else:
            flash('No account.', 'warning')
    return render_template('auth/login.html', form=form)  #


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout success.', 'info')
    return redirect(url_for('message.index'))
