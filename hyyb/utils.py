# -*- coding: utf-8 -*-
"""
Created on Fri Apr 11 06:58:04 2025

@author: Administrator
"""
try:
    from urlparse import urlparse, urljoin
except ImportError:
    from urllib.parse import urlparse, urljoin

from flask import request, redirect, url_for, current_app
import pandas as pd
from sqlalchemy import create_engine
import os
import uuid

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def redirect_back(default='message.index', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['BLUELOG_ALLOWED_IMAGE_EXTENSIONS']



def import_excel_to_database(excel_file, table_name):
    db_url = current_app.config['SQLALCHEMY_DATABASE_URI']
    engine = create_engine(db_url)
    data = pd.read_excel(excel_file)
    data.to_sql(table_name, engine, if_exists='append', index=False)


def export_db_to_excel(*table_names, excel_file):
    db_url = current_app.config['SQLALCHEMY_DATABASE_URI']
    engine = create_engine(db_url)
    with pd.ExcelWriter(excel_file) as writer:
        for table_name in table_names:
            data = pd.read_sql_query(f"SELECT * FROM {table_name}", engine)
            data.to_excel(writer, sheet_name=table_name, index=False)


def rename_filename(filename, new_filename):
    ext = os.path.splitext(filename)[1]
    return new_filename + ext