from flask import render_template, flash, redirect, url_for, request, \
    current_app, Blueprint, abort, make_response
from flask_login import current_user, login_required

from hyyb.extensions import db
from hyyb.forms import AttendanceForm
from hyyb.models import Stuff, Attendance
from hyyb.utils import redirect_back

attendance_bp = Blueprint('attendance', __name__)


@attendance_bp.route('/attendance/new', methods=['GET', 'POST'])
@login_required
def attendance_new():
    form = AttendanceForm()
    if form.validate_on_submit():
        stuff = Stuff.query.get(form.stuff.data)
        datestamp = form.datestamp.data
        am = form.am.data
        pm = form.pm.data
        trip = form.trip.data
        othr = form.othr.data

        attendance = Attendance(stuff=stuff,
                                datestamp=datestamp,
                                am=am,
                                pm=pm,
                                trip=trip,
                                othr=othr)
        db.session.add(attendance)
        db.session.commit()
        flash('出勤记录已经创建！', 'success')
        return redirect(url_for('attendance.attendance_manage'))
    return render_template('attendance/attendance_new.html', form=form)


@attendance_bp.route('/attendance/manage', methods=['GET', 'POST'])
@login_required
def attendance_manage():
    page = request.args.get('page', 1, type=int)
    pagination = Attendance.query.order_by(Attendance.datestamp.desc()).paginate(
        page, per_page=current_app.config['HYYB_ATTENDANCE_MANAGE_PER_PAGE'])
    attendances = pagination.items
    return render_template('attendance/attendance_manage.html',
                           page=page,
                           pagination=pagination,
                           attendances=attendances)


@attendance_bp.route('/attendance/view', methods=['GET', 'POST'])
@login_required
def attendance_view():
    page = request.args.get('page', 1, type=int)
    pagination = Attendance.query.order_by(Attendance.datestamp.desc()).paginate(
        page, per_page=current_app.config['HYYB_ATTENDANCE_PER_PAGE'])
    attendances = pagination.items
    return render_template('attendance/attendance_view.html',
                           page=page,
                           pagination=pagination,
                           attendances=attendances)


@attendance_bp.route('/attendance/delete/<int:attendance_id>',  methods=['POST'])
@login_required
def attendance_delete(attendance_id):
    attendance = Attendance.query.get_or_404(attendance_id)
    db.session.delete(attendance)
    db.session.commit()
    flash('删除了出勤记录！', 'success')
    return redirect(url_for('attendance.attendance_manage'))


@attendance_bp.route('/attendance/edit/<int:attendance_id>', methods=['GET', 'POST'])
@login_required
def attendance_edit(attendance_id):
    form = AttendanceForm()
    attendance = Attendance.query.get_or_404(attendance_id)
    if form.validate_on_submit():
       # attendance.stuff = Stuff.query.get(form.stuff.data)
        attendance.stuff = attendance.stuff
        attendance.datestamp = form.datestamp.data
        attendance.am = form.am.data
        attendance.pm = form.pm.data
        attendance.trip = form.trip.data
        attendance.othr = form.othr.data
        db.session.commit()
        flash('修改了出勤记录！', 'success')
        return redirect(url_for('attendance.attendance_manage'))
    form.stuff.data = attendance.stuff_id
    form.datestamp.data = attendance.datestamp
    form.am.data = attendance.am
    form.pm.data = attendance.pm
    form.trip.data = attendance.trip
    form.othr.data = attendance.othr
    return render_template('attendance/attendance_edit.html', form=form, attendance=attendance)
