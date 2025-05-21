from flask import render_template, flash, redirect, url_for, request, current_app, \
    Blueprint, request, abort, make_response
from flask_login import current_user, login_required

from hyyb.extensions import db
from hyyb.forms import DiaryForm
from hyyb.models import Diary, Jobcategory
from hyyb.utils import redirect_back

diary_bp = Blueprint('diary', __name__)


@diary_bp.route('/diary/new', methods=['GET', 'POST'])
@login_required
def diary_new():
    form = DiaryForm()
    if form.validate_on_submit():
        worker = form.worker.data
        start_time = form.start_time.data
        end_time = form.end_time.data
        content = form.content.data
        jobcategory = Jobcategory.query.get(form.jobcategory.data)
        auditor = form.auditor.data
        datestamp = form.datestamp.data
        factor = form.factor.data
        others = form.others.data
        diary = Diary(worker=worker,
                      start_time=start_time,
                      end_time=end_time,
                      content=content,
                      jobcategory=jobcategory,
                      auditor=auditor,
                      datestamp=datestamp,
                      factor=factor,
                      others=others)
        db.session.add(diary)
        db.session.commit()
        flash('创建了工作日志！', 'success')
        return redirect(url_for('diary.diary_manage'))
    return render_template('diary/diary_new.html', form=form)


@diary_bp.route('/diary/edit/<int:diary_id>', methods=['GET', 'POST'])
@login_required
def diary_edit(diary_id):
    form = DiaryForm()
    diary = Diary.query.get_or_404(diary_id)
    if form.validate_on_submit():
        diary.worker = form.worker.data
        diary.start_time = form.start_time.data
        diary.end_time = form.end_time.data
        diary.content = form.content.data
  #      diary.jobcategory = Jobcategory.query.get(form.jobcategory.data)
        diary.jobcategory = diary.jobcategory
        diary.auditor = form.auditor.data
        diary.datestamp = form.datestamp.data
        diary.factor = form.factor.data
        diary.othr = form.othr.data
        db.session.commit()
        flash('修改了工作日志！', 'success')
        return redirect(url_for('diary.diary_manage'))
    form.worker.data = diary.worker
    form.start_time.data = diary.start_time
    form.end_time.data = diary.end_time
    form.content.data = diary.content
    form.jobcategory.data = diary.jobcategory_id
    form.auditor.data = diary.auditor
    form.datestamp.data = diary.datestamp
    form.factor.data = diary.factor
    form.othr.data = diary.othr
    return render_template('diary/diary_edit.html', form=form)


@diary_bp.route('/diary/delete/<int:diary_id>', methods=['GET', 'POST'])
@login_required
def diary_delete(diary_id):
    diary = Diary.query.get_or_404(diary_id)
    db.session.delete(diary)
    db.session.commit()
    flash('删除了工作日志！', 'success')
    return redirect(url_for('diary.diary_manage'))


@diary_bp.route('/diary/manage', methods=['GET', 'POST'])
@login_required
def diary_manage():
    page = request.args.get('page', 1, type=int)
    pagination = Diary.query.order_by(Diary.datestamp.desc()).paginate(
        page=page, per_page=current_app.config['HYYB_DIARY_MANAGE_PER_PAGE'])
    diaries = pagination.items
    return render_template('diary/diary_manage.html',
                           page=page,
                           pagination=pagination,
                           diaries=diaries)


@diary_bp.route('/diary/view', methods=['GET', 'POST'])
@login_required
def diary_view():
    page = request.args.get('page', 1, type=int)
    pagination = Diary.query.order_by(Diary.datestamp.desc()).paginate(
        page=page, per_page=current_app.config['HYYB_DIARY_PER_PAGE'])
    diaries = pagination.items
    return render_template('diary/diary_view.html',
                           page=page,
                           pagination=pagination,
                           diaries=diaries)
