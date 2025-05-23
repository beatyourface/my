# -*- coding: utf-8 -*-
"""
Created on Wed Apr  9 07:35:44 2025

@author: Administrator
"""
from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from hyyb.extensions import db


class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(256))
    privilege = db.Column(db.Integer, default=0)
    title = db.Column(db.String(60))
    othr = db.Column(db.String(60))

    stuff = db.relationship('Stuff', back_populates='admin',  uselist=False)

    def set_password(self, password='123456'):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class Stuff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    num = db.Column(db.Integer, unique=True)
    designation = db.Column(db.String(20), index=True, unique=True)
    gendar = db.Column(db.Boolean, default=True)
    dcome = db.Column(db.Date)
    school = db.Column(db.String(60))
    degree = db.Column(db.String(60))
    phone = db.Column(db.String(20))
    addr = db.Column(db.String(100))
    team = db.Column(db.Integer)
    situation = db.Column(db.String(20))
    manage = db.Column(db.Boolean, default=False)
    othr = db.Column(db.String(60))

    attendances = db.relationship('Attendance', back_populates='stuff')

    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    department = db.relationship('Department', back_populates='stuffs')

    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    admin = db.relationship('Admin', back_populates='stuff')


class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datestamp = db.Column(db.Date, index=True)
    am = db.Column(db.Boolean, default=True)
    pm = db.Column(db.Boolean, default=True)
    trip = db.Column(db.Boolean, default=False)
    othr = db.Column(db.String(60))

    stuff_id = db.Column(db.Integer, db.ForeignKey('stuff.id'))
    stuff = db.relationship('Stuff', back_populates='attendances')


class Hazard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    content = db.Column(db.Text)
    material = db.Column(db.Text)
    material_ok = db.Column(db.Boolean, default=False)
    director = db.Column(db.String(20))
    cooperators = db.Column(db.String(100))
    scheme = db.Column(db.Text)
    leader = db.Column(db.String(20))
    othr = db.Column(db.String(60))
    onstop = db.Column(db.Boolean, default=False)

    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    department = db.relationship('Department', back_populates='hazards')


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    designation = db.Column(db.String(20))
    othr = db.Column(db.String(60))

    hazards = db.relationship('Hazard', back_populates='department')
    stuffs = db.relationship('Stuff', back_populates='department')

    def delete(self):
        default_department = Department.query.get(1)

        hazards = self.hazards[:]
        for hazard in hazards:
            hazard.department = default_department

        stuffs = self.stuffs[:]
        for stuff in stuffs:
            stuff.department = default_department

        db.session.delete(self)
        db.session.commit()


class Spare(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    designation = db.Column(db.String(80), index=True)
    model = db.Column(db.String(80))
    quantity = db.Column(db.Integer)
    unit = db.Column(db.String(20))
    purpose = db.Column(db.String(60))
    shelve = db.Column(db.Integer)
    rack = db.Column(db.Integer)
    serialnum = db.Column(db.Integer)
    place = db.Column(db.String(60))
    price = db.Column(db.Float)
    othr = db.Column(db.String(60))

    departmentp_id = db.Column(db.Integer, db.ForeignKey('departmentp.id'))
    departmentp = db.relationship('Departmentp', back_populates='spares')

    opts = db.relationship('Opt', back_populates='spare')

    def delete(self):
        default_spare = Spare.query.get(1)
        opts = self.opts[:]
        for opt in opts:
            opt.spare = default_spare
        db.session.delete(self)
        db.session.commit()


class Departmentp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    designation = db.Column(db.String(20))
    othr = db.Column(db.String(60))

    spares = db.relationship('Spare', back_populates='departmentp')

    def delete(self):
        default_departmentp = Departmentp.query.get(1)
        spares = self.spares[:]
        for spare in spares:
            spare.departmentp = default_departmentp
        db.session.delete(self)
        db.session.commit()


class Diary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    worker = db.Column(db.String(20))
    content = db.Column(db.Text)
    auditor = db.Column(db.String(20))
    datestamp = db.Column(db.Date, index=True)
    factor = db.Column(db.Float)
    othr = db.Column(db.String(60))

    jobcategory_id = db.Column(db.Integer, db.ForeignKey('jobcategory.id'))
    jobcategory = db.relationship('Jobcategory', back_populates='diaries')


class Jobcategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    designation = db.Column(db.String(80), unique=True)
    score = db.Column(db.Float)
    othr = db.Column(db.String(60))

    diaries = db.relationship('Diary', back_populates='jobcategory')

    def delete(self):
        default_jobcategory = Jobcategory.query.get(1)
        diaries = self.diaries[:]
        for diary in diaries:
            diary.jobcategory = default_jobcategory
        db.session.delete(self)
        db.session.commit()


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    designation = db.Column(db.String(20))
    body = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    author = db.Column(db.String(20))
    othr = db.Column(db.String(60))


class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    designation = db.Column(db.String(30))
    url = db.Column(db.String(255))


class Opt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    author = db.Column(db.String(20))
    obtain = db.Column(db.Integer, default=1)
    quantity = db.Column(db.Integer)
    othr = db.Column(db.String(60))

    spare_id = db.Column(db.Integer, db.ForeignKey('spare.id'))
    spare = db.relationship('Spare', back_populates='opts')

class Seek(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    selector0 = db.Column(db.Integer, default=1)
    designation1 = db.Column(db.String(20), default='')
    designation2 = db.Column(db.String(20), default='')
    designation3 = db.Column(db.String(20), default='')
    designation4 = db.Column(db.String(20), default='')