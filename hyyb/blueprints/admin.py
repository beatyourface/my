import os

from flask import render_template, flash, redirect, url_for, request, current_app, Blueprint, send_from_directory
from flask_login import login_required, current_user
from flask_ckeditor import upload_success, upload_fail

from hyyb.extensions import db
from hyyb.models import Link, Jobcategory, Department, Departmentp, Spare, Seek
from hyyb.forms import SettingForm, LinkForm, JobcategoryForm, DepartmentpForm, DepartmentForm,\
    SeekForm

from hyyb.utils import redirect_back, allowed_file

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = SettingForm()
    if form.validate_on_submit():
        current_user.title = form.title.data
        current_user.othr = form.othr.data
        db.session.commit()
        flash('Setting updated.', 'success')
        return redirect(url_for('message.index'))
    form.title.data = current_user.title
    form.othr.data = current_user.othr
    return render_template('admin/settings.html', form=form)


@admin_bp.route('/link/manage')
@login_required
def manage_link():
    return render_template('admin/manage_link.html')


@admin_bp.route('/link/new', methods=['GET', 'POST'])
@login_required
def new_link():
    form = LinkForm()
    if form.validate_on_submit():
        designation = form.designation.data
        url = form.url.data
        link = Link(designation=designation, url=url)
        db.session.add(link)
        db.session.commit()
        flash('Link created.', 'success')
        return redirect(url_for('.manage_link'))
    return render_template('admin/new_link.html', form=form)


@admin_bp.route('/link/<int:link_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_link(link_id):
    form = LinkForm()
    link = Link.query.get_or_404(link_id)
    if form.validate_on_submit():
        link.designation = form.designation.data
        link.url = form.url.data
        db.session.commit()
        flash('Link updated.', 'success')
        return redirect(url_for('.manage_link'))

    form.designation.data = link.designation
    form.url.data = link.url
    return render_template('admin/edit_link.html', form=form)


@admin_bp.route('/link/<int:link_id>/delete', methods=['POST'])
@login_required
def delete_link(link_id):
    link = Link.query.get_or_404(link_id)
    db.session.delete(link)
    db.session.commit()
    flash('Link deleted.', 'success')
    return redirect(url_for('.manage_link'))


@admin_bp.route('/jobcategory/manage')
@login_required
def manage_jobcategory():
    page = request.args.get('page', 1, type=int)
    pagination = Jobcategory.query.order_by(Jobcategory.id).paginate(
        page, per_page=current_app.config['HYYB_JOBCATEGORY_MANAGE_PER_PAGE'])  # 分页
    jobcategories = pagination.items
    return render_template('admin/manage_jobcategory.html',
                           page=page,
                           pagination=pagination,
                           jobcategories=jobcategories)


@admin_bp.route('/jobcategory/new', methods=['GET', 'POST'])
@login_required
def new_jobcategory():
    form = JobcategoryForm()
    if form.validate_on_submit():
        designation = form.designation.data
        score = form.score.data
        othr = form.othr.data
        jobcategory = Jobcategory(designation=designation, score=score, othr=othr)
        db.session.add(jobcategory)
        db.session.commit()
        flash('工作分类已经添加.', 'success')
        return redirect(url_for('.manage_jobcategory'))
    return render_template('admin/new_jobcategory.html', form=form)


@admin_bp.route('/jobcategory/<int:jobcategory_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_jobcategory(jobcategory_id):
    form = JobcategoryForm()
    jobcategory = Jobcategory.query.get_or_404(jobcategory_id)
    if jobcategory.id == 1:
        flash('不能编辑默认分类.', 'warning')
    if form.validate_on_submit():
        jobcategory.designation = form.designation.data
        jobcategory.score = form.score.data
        jobcategory.othr = form.othr.data
        db.session.commit()
        flash('工作分类已经更新.', 'success')
        return redirect(url_for('.manage_jobcategory'))

    form.designation.data = jobcategory.designation
    form.score.data = jobcategory.score
    form.othr.data = jobcategory.othr
    return render_template('admin/edit_jobcategory.html', form=form)


@admin_bp.route('/jobcategory/<int:jobcategory_id>/delete', methods=['POST'])
@login_required
def delete_jobcategory(jobcategory_id):
    jobcategory = Jobcategory.query.get_or_404(jobcategory_id)
    if jobcategory.id == 1:
        flash('不能删除默认分类.', 'warning')
        return redirect(url_for('.manage_jobcategory'))
    jobcategory.delete()
    flash('工作分类已经删除.', 'success')
    return redirect(url_for('.manage_jobcategory'))  # 重定向到分类管理页面


@admin_bp.route('/department/manage')
@login_required
def manage_department():
    return render_template('admin/manage_department.html')


@admin_bp.route('/department/new', methods=['GET', 'POST'])
@login_required
def new_department():
    form = DepartmentForm()
    if form.validate_on_submit():
        designation = form.designation.data
        othr = form.othr.data
        department = Department(designation=designation, othr=othr)
        db.session.add(department)
        db.session.commit()
        flash('部门已经创建.', 'success')
        return redirect(url_for('.manage_department'))

    return render_template('admin/new_department.html', form=form)


@admin_bp.route('/department/<int:department_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_department(department_id):
    form = DepartmentForm()
    department = Department.query.get_or_404(department_id)
    if form.validate_on_submit():
        department.designation = form.designation.data
        department.othr = form.othr.data
        db.session.commit()
        flash('部门已经更新.', 'success')
        return redirect(url_for('.manage_department'))

    form.designation.data = department.designation
    form.othr.data = department.othr
    return render_template('admin/edit_department.html', form=form)


@admin_bp.route('/department/<int:department_id>/delete', methods=['POST'])
@login_required
def delete_department(department_id):
    department = Department.query.get_or_404(department_id)
    if department.id == 1:
        flash('不能删除默认车间部门', 'warning')
        return redirect(url_for('.manage_department'))
    department.delete()
    flash('车间部门已经删除', 'success')
    return redirect(url_for('.manage_department'))


@admin_bp.route('/departmentp/manage')
@login_required
def manage_departmentp():
    return render_template('admin/manage_departmentp.html')


@admin_bp.route('/departmentp/new', methods=['GET', 'POST'])
@login_required
def new_departmentp():
    form = DepartmentpForm()
    if form.validate_on_submit():
        designation = form.designation.data
        othr = form.othr.data
        departmentp = Departmentp(designation=designation, othr=othr)
        db.session.add(departmentp)
        db.session.commit()
        flash('仓库已经创建.', 'success')
        return redirect(url_for('.manage_departmentp'))

    return render_template('admin/new_departmentp.html', form=form)


@admin_bp.route('/departmentp/<int:departmentp_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_departmentp(departmentp_id):
    form = DepartmentpForm()
    departmentp = Departmentp.query.get_or_404(departmentp_id)
    if form.validate_on_submit():
        departmentp.designation = form.designation.data
        departmentp.othr = form.othr.data
        db.session.commit()
        flash('仓库已经更新.', 'success')
        return redirect(url_for('.manage_departmentp'))

    form.designation.data = departmentp.designation
    form.othr.data = departmentp.othr
    return render_template('admin/edit_departmentp.html', form=form)


@admin_bp.route('/departmentp/<int:departmentp_id>/delete', methods=['POST'])
@login_required
def delete_departmentp(departmentp_id):
    departmentp = Departmentp.query.get_or_404(departmentp_id)
    if departmentp.id == 1:
        flash('不能删除默认仓库', 'warning')
        return redirect(url_for('.manage_departmentp'))
    departmentp.delete()
    flash('仓库已经删除.', 'success')
    return redirect(url_for('.manage_departmentp'))


@admin_bp.route('/departmentp/<int:departmentp_id>', methods=['GET', 'POST'])
#@login_required
def show_departmentp(departmentp_id):
    departmentp = Departmentp.query.get_or_404(departmentp_id)
    page = request.args.get('page', 1, type=int)

    seek_form = SeekForm()
    seek = Seek.query.get_or_404(1)
    if seek_form.validate_on_submit():
        seek.designation2 = seek_form.designation2.data
        page = 1
        db.session.commit()
    #        flash('搜索成功！','success')

    desgination2 = seek.designation2
    seek_form.designation2.data = seek.designation2

    per_page = current_app.config['HYYB_DEPARTMENTP_PER_PAGE']
    pagination = Spare.query.with_parent(departmentp).order_by(Spare.shelve.asc()).order_by(Spare.rack.asc()).order_by(Spare.serialnum.asc()).\
        filter(Spare.designation.like('%' + desgination2 + '%')).paginate(page, per_page)
    spares = pagination.items

    if not spares:
        flash('没有找到符合条件的备件记录！', 'warning')
        seek.designation2 = ''
        db.session.commit()
        return redirect(url_for('.show_departmentp', departmentp_id=departmentp_id))

    return render_template('admin/show_departmentp.html',
                           departmentp=departmentp, page=page,
                           pagination=pagination, spares=spares,
                           seek_form=seek_form)


@admin_bp.route('/uploads/<path:filename>')
def get_image(filename):
    return send_from_directory(current_app.config['HYYB_UPLOAD_PATH'], filename)


@admin_bp.route('/upload', methods=['POST'])
def upload_image():
    f = request.files.get('upload')
    if not allowed_file(f.filename):
        return upload_fail('Image only!')
    f.save(os.path.join(current_app.config['HYYB_UPLOAD_PATH'], f.filename))
    url = url_for('.get_image', filename=f.filename)
    return upload_success(url, f.filename)
