# -*- coding: utf-8 -*-
"""
Created on Wed Apr  9 15:57:38 2025

@author: Administrator
"""
import os
import sys, pymysql

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

#Mysql URI
user = "hyhg"
pwd = "hyhg123456"
host = "localhost"
dbn = "hyhg"


class BaseConfig(object):
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev key')

    DEBUG_TB_INTERCEPT_REDIRECTS = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    CKEDITOR_ENABLE_CSRF = True
    CKEDITOR_FILE_UPLOADER = 'admin.upload_image'

    # MAIL_SERVER = os.getenv('MAIL_SERVER')
    # MAIL_PORT = 465
    # MAIL_USE_SSL = True
    # MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    # MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    # MAIL_DEFAULT_SENDER = ('Bluelog Admin', MAIL_USERNAME)

    # HYYB_EMAIL = os.getenv('HYYB_EMAIL')
    HYYB_MESSAGE_PER_PAGE = 15
    HYYB_MESSAGE_MANAGE_PER_PAGE = 10

    HYYB_DIARY_PER_PAGE = 15
    HYYB_DIARY_MANAGE_PER_PAGE = 10

    HYYB_SPARE_PER_PAGE = 15
    HYYB_SPARE_MANAGE_PER_PAGE = 10

    HYYB_ATTENDANCE_PER_PAGE = 15
    HYYB_ATTENDANCE_MANAGE_PER_PAGE = 10

    HYYB_HAZARD_PER_PAGE = 15
    HYYB_HAZARD_MANAGE_PER_PAGE = 10

    HYYB_JOBCATEGORY_PER_PAGE = 15
    HYYB_JOBCATEGORY_MANAGE_PER_PAGE = 10

    HYYB_DEPARTMENT_PER_PAGE = 15
    HYYB_DEPARTMENT_MANAGE_PER_PAGE = 10

    HYYB_DEPARTMENTP_PER_PAGE = 15
    HYYB_DEPARTMENTP_MANAGE_PER_PAGE = 10

    HYYB_OPT_PER_PAGE = 15
    HYYB_OPT_MANAGE_PER_PAGE = 10

    HYYB_POST_PER_PAGE = 10
    HYYB_MANAGE_POST_PER_PAGE = 15
    HYYB_COMMENT_PER_PAGE = 15
    # ('theme name', 'display name')
    HYYB_THEMES = {'perfect_blue': 'Perfect Blue', 'black_swan': 'Black Swan'}
    HYYB_SLOW_QUERY_THRESHOLD = 1

    HYYB_UPLOAD_PATH = os.path.join(basedir, 'uploads')
    HYYB_DOWNLOAD_PATH = os.path.join(basedir, 'downloads')
    HYYB_ALLOWED_IMAGE_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']
    HYYB_ALLOWED_EXCEL_EXTENSIONS = ['xlsx']

    # Flask-CKEditor config
    CKEDITOR_SERVE_LOCAL = True
    CKEDITOR_FILE_UPLOADER = 'message.upload_for_ckeditor'

    HYYB_MAX_CONTENT_LENGTH = 3 * 1024 * 1024

class DevelopmentConfig(BaseConfig):
 #  SQLALCHEMY_DATABASE_URI = prefix + os.path.join(basedir, 'data-dev.db')
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{user}:{pwd}@{host}:3306/{dbn}?charset=utf8mb4'

class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # in-memory database


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', prefix + os.path.join(basedir, 'data.db'))


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
