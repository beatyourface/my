from urllib import request

from flask import render_template, flash, redirect, url_for, Blueprint, current_app, \
    request, make_response, abort, send_from_directory, session
from flask_login import login_required, current_user

from hyyb.forms import MessageForm
from hyyb.models import Message, Seek
from hyyb.extensions import db
from hyyb.utils import redirect_back
import os
from flask_ckeditor import upload_success, upload_fail


message_bp = Blueprint('message', __name__)


@message_bp.route('/', methods=['GET', 'POST'])
def index():
    seek = Seek.query.get_or_404(1)
    seek.designation1 = ''
    seek.designation2 = ''
    seek.designation3 = ''
    seek.designation4 = ''
    db.session.commit()

    page = request.args.get('page', 1, type=int)
    pagination = Message.query.order_by(Message.timestamp.desc()).paginate(
        page=page, per_page=current_app.config['HYYB_MESSAGE_PER_PAGE'])
    messages = pagination.items
    return render_template('message/message_view.html',
                           page=page,
                           pagination=pagination,
                           messages=messages)


@message_bp.route('/message/new', methods=['GET', 'POST'])
@login_required
def message_new():
    form = MessageForm()
    if form.validate_on_submit():
        designation = form.designation.data
        body = form.body.data
        author = current_user.stuff.designation
        othr = form.othr.data
        message = Message(designation=designation, body=body, author=author, othr=othr)
        db.session.add(message)
        db.session.commit()
        flash('消息已经创建！', 'success')
        return redirect(url_for('message.message_manage'))
    return render_template('message/message_new.html', form=form)


@message_bp.route('/message/<int:message_id>/edit', methods=['GET', 'POST'])
@login_required
def message_edit(message_id):
    form = MessageForm()
    message = Message.query.get_or_404(message_id)
    if form.validate_on_submit():
        message.designation = form.designation.data
        message.body = form.body.data
        message.author = current_user.stuff.designation
        message.othr = form.othr.data
        db.session.commit()
        flash('消息已经修改！', 'success')
        return redirect(url_for('message.message_manage'))
    form.designation.data = message.designation
    form.body.data = message.body
    form.othr.data = message.othr
    return render_template('message/message_edit.html', form=form)


@message_bp.route('/message/<int:message_id>/delete', methods=['POST'])
@login_required
def message_delete(message_id):
    message = Message.query.get_or_404(message_id)
    db.session.delete(message)
    db.session.commit()
    flash('消息已经删除！', 'success')
    return redirect(url_for('message.message_manage'))


@message_bp.route('/message/manage', methods=['GET', 'POST'])
@login_required
def message_manage():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['HYYB_MESSAGE_MANAGE_PER_PAGE']
    pagination = Message.query.order_by(Message.timestamp.desc()).paginate(page=page, per_page=per_page)
    messages = pagination.items
    return render_template('message/message_manage.html',
                           page=page,
                           pagination=pagination,
                           messages=messages)


@message_bp.route('/change-theme/<theme_name>')
def change_theme(theme_name):
    if theme_name not in current_app.config['HYYB_THEMES'].keys():
        abort(404)

    response = make_response(redirect_back())
    response.set_cookie('theme', theme_name, max_age=30 * 24 * 60 * 60)
    return response


@message_bp.route('/message/uploads/<path:filename>')
def get_file(filename):
    return send_from_directory(current_app.config['HYYB_UPLOAD_PATH'], filename)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['HYYB_ALLOWED_IMAGE_EXTENSIONS']


# handle image upload for ckeditor
@message_bp.route('/message/upload-ck', methods=['POST'])
def upload_for_ckeditor():
    f = request.files.get('upload')
    if not allowed_file(f.filename):
        return upload_fail('Image only!')
    f.save(os.path.join(current_app.config['HYYB_UPLOAD_PATH'], f.filename))
    url = url_for('get_file', filename=f.filename)
    return upload_success(url, f.filename)
