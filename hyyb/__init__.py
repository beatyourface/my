# -*- coding: utf-8 -*-
"""
Created on Fri Apr 11 06:59:31 2025

@author: Administrator
"""
import logging
import os
from logging.handlers import SMTPHandler, RotatingFileHandler

import click
from flask import Flask, render_template, request
from flask_login import current_user
from flask_sqlalchemy import record_queries
from flask_wtf.csrf import CSRFError

from hyyb.blueprints.admin import admin_bp
from hyyb.blueprints.attendance import attendance_bp
from hyyb.blueprints.auth import auth_bp
from hyyb.blueprints.diary import diary_bp
from hyyb.blueprints.hazard import hazard_bp
from hyyb.blueprints.message import message_bp
from hyyb.blueprints.spare import spare_bp
from hyyb.extensions import bootstrap, db, login_manager, csrf, ckeditor, moment, toolbar #, migrate
from hyyb.models import Admin, Stuff, Attendance, Diary, Hazard, Spare, Message, Departmentp, \
    Department, Link, Jobcategory
from hyyb.settings import config


basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('hyyb')
    app.config.from_object(config[config_name])

    register_logging(app)
    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    register_errors(app)
    register_shell_context(app)
    register_template_context(app)
    register_request_handlers(app)
    return app


def register_logging(app):
    class RequestFormatter(logging.Formatter):

        def format(self, record):
            record.url = request.url
            record.remote_addr = request.remote_addr
            return super(RequestFormatter, self).format(record)

    request_formatter = RequestFormatter(
        '[%(asctime)s] %(remote_addr)s requested %(url)s\n'
        '%(levelname)s in %(module)s: %(message)s'
    )

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler = RotatingFileHandler(os.path.join(basedir, 'logs/bluelog.log'),
                                       maxBytes=10 * 1024 * 1024, backupCount=10)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    if not app.debug:
        app.logger.addHandler(file_handler)


def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    ckeditor.init_app(app)
    moment.init_app(app)
    toolbar.init_app(app)
  #  migrate.init_app(app, db)


def register_blueprints(app):
    app.register_blueprint(message_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(diary_bp, url_prefix='/diary')
    app.register_blueprint(hazard_bp, url_prefix='/hazard')
    app.register_blueprint(spare_bp, url_prefix='/spare')
    app.register_blueprint(attendance_bp, url_prefix='/attendance')


def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
        db.create_all()
        click.echo('Initialized database.')

    @app.cli.command()
    @click.option('--username', prompt=True, help='The username used to login.')
    @click.option('--password', prompt=True, hide_input=True,
                  confirmation_prompt=True, help='The password used to login.')
    def init(username, password):
        """Building hyyb, just for you."""

        click.echo('Initializing the database...')
        db.create_all()

        admin = Admin.query.first()
        if admin is not None:
            click.echo('The administrator already exists, updating...')
            admin.username = username
            admin.set_password(password)
        else:
            click.echo('Creating the temporary administrator account...')
            admin = Admin(
                username='admin',
                privilege=1,
                title="No, I'm the real thing.",
                othr='Um, l, Mima Kirigoe, had a fun time as a member of CHAM...'
            )
            admin.set_password(password)
            db.session.add(admin)

        jobcategory = Jobcategory.query.first()
        if jobcategory is None:
            click.echo('Creating the default jobcategory...')
            jobcategory = Jobcategory(designation='Default')
            db.session.add(jobcategory)

        db.session.commit()
        click.echo('Done.')

    @app.cli.command()
    @click.option('--jobcategory', default=10, help='Quantity of categories, default is 10.')
    @click.option('--department', default=10, help='Quantity of departments, default is 10.')
    @click.option('--departmentp', default=10, help='Quantity of departmentps, default is 10.')
    @click.option('--stuff', default=50, help='Quantity of stuffs, default is 10.')
    @click.option('--admini', default=50, help='Quantity of stuffs, default is 10.')
    @click.option('--message', default=30, help='Quantity of messages, default is 10.')
    @click.option('--hazard', default=60, help='Quantity of hazards, default is 10.')
    @click.option('--spare', default=80, help='Quantity of spares, default is 10.')
    @click.option('--attendance', default=150, help='Quantity of attendances, default is 10.')
    @click.option('--diary', default=100, help='Quantity of diarys, default is 10.')
    @click.option('--opt', default=60, help='Quantity of diarys, default is 10.')
    def forge(jobcategory, department, departmentp, stuff, admini, message, hazard, spare, attendance, diary, opt):
        """Generate fake data."""
        from hyyb.fakes import fake_admins, fake_jobcategories, fake_links, fake_messages, fake_departments, \
            fake_stuffs, fake_departmentps, fake_attendances, fake_hazards, fake_spares, fake_diaries, fake_opts,\
            fake_seek

        db.drop_all()
        db.create_all()

        click.echo('Generating %d categories...' % jobcategory)
        fake_jobcategories(jobcategory)

        click.echo('Generating %d departments...' % department)
        fake_departments(department)

        click.echo('Generating %d departmentps...' % departmentp)
        fake_departmentps(departmentp)

        click.echo('Generating %d stuffs...' % stuff)
        fake_stuffs(stuff)

        click.echo('Generating %d  administrators...' % admini)
        fake_admins(admini)

        click.echo('Generating %d attendances...' % attendance)
        fake_attendances(attendance)

        click.echo('Generating %d hazards...' % hazard)
        fake_hazards(hazard)

        click.echo('Generating %d spares...' % spare)
        fake_spares(spare)

        click.echo('Generating %d diaries...' % diary)
        fake_diaries(diary)

        click.echo('Generating links...')
        fake_links()

        click.echo('Generating %d messages...' % message)
        fake_messages(message)

        click.echo('Generating %d opts...' % opt)
        fake_opts(opt)

        click.echo('Generating seek')
        fake_seek()


        click.echo('Done.')


def register_template_context(app):
    @app.context_processor
    def make_template_context():
        admin = current_user
        jobcategories = Jobcategory.query.order_by(Jobcategory.designation).all()
        links = Link.query.order_by(Link.id).all()
        messages = Message.query.order_by(Message.timestamp).all()
        departments = Department.query.order_by(Department.id).all()
        departmentps = Departmentp.query.order_by(Departmentp.id).all()

        return dict(admin=admin,
                    jobcategoryies=jobcategories,
                    links=links,
                    messages=messages,
                    departments=departments,
                    departmentps=departmentps)


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db,
                    Admin=Admin,
                    Stuff=Stuff,
                    Attendance=Attendance,
                    Diary=Diary,
                    Hazard=Hazard,
                    Spare=Spare,
                    Message=Message,
                    Departmentp=Departmentp,
                    Department=Department,
                    Link=Link,
                    Jobcategory=Jobcategory)


def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_template('errors/400.html', description=e.description), 400


def register_request_handlers(app):
    @app.after_request
    def query_profiler(response):
        for q in record_queries.get_recorded_queries ():
            if q.duration >= app.config['HYYB_SLOW_QUERY_THRESHOLD']:
                app.logger.warning(
                    'Slow query: Duration: %fs\n Context: %s\nQuery: %s\n '
                    % (q.duration, q.context, q.statement)
                )
        return response

app = create_app('production')
if __name__ == "__main__":
        app.run()
