from flask import render_template, flash, redirect, url_for, request, current_app, Blueprint, abort, make_response
from flask_login import current_user, login_required

from hyyb.extensions import db
from hyyb.forms import HazardForm
from hyyb.models import Hazard, Department

hazard_bp = Blueprint('hazard', __name__)


@hazard_bp.route('/hazard/new', methods=['GET', 'POST'])
@login_required
def hazard_new():
    form = HazardForm()
    if form.validate_on_submit():
        department = Department.query.get(form.department.data)
        content = form.content.data
        material = form.material.data
        material_ok = form.material_ok.data
        director = form.director.data
        cooperators = form.cooperators.data
        scheme = form.scheme.data
        leader = form.leader.data
        othr = form.othr.data
        onstop = form.onstop.data

        hazard = Hazard(department=department,
                        content=content,
                        material=material,
                        material_ok=material_ok,
                        director=director,
                        cooperators=cooperators,
                        scheme=scheme,
                        leader=leader,
                        othr=othr,
                        onstop=onstop
                        )
        db.session.add(hazard)
        db.session.commit()
        flash('隐患已经新建！', 'success')
        return redirect(url_for('hazard.hazard_manage'))
    return render_template('hazard/hazard_new.html', form=form)


@hazard_bp.route('/hazard/<int:hazard_id>/edit', methods=['GET', 'POST'])
@login_required
def hazard_edit(hazard_id):
    form = HazardForm()
    hazard = Hazard.query.get_or_404(hazard_id)
    if form.validate_on_submit():
    #    hazard.department = Department.query.get(form.department.data)
        hazard.department = hazard.department
        hazard.content = form.content.data
        hazard.material = form.material.data
        hazard.material_ok = form.material_ok.data
        hazard.director = form.director.data
        hazard.cooperators = form.cooperators.data
        hazard.scheme = form.scheme.data
        hazard.leader = form.leader.data
        hazard.othr = form.othr.data
        hazard.onstop = form.onstop.data
        db.session.commit()
        flash('隐患已经修改！', 'success')
        return redirect(url_for('hazard.hazard_manage'))
    form.department.data = hazard.department_id
    form.content.data = hazard.content
    form.material.data = hazard.material
    form.material_ok.data = hazard.material_ok
    form.director.data = hazard.director
    form.scheme.data = hazard.scheme
    form.leader.data = hazard.leader
    form.othr.data = hazard.othr
    form.onstop.data = hazard.onstop
    return render_template('hazard/hazard_edit.html', form=form)


@hazard_bp.route('/hazard/<int:hazard_id>/delete', methods=['GET', 'POST'])
@login_required
def hazard_delete(hazard_id):
    hazard = Hazard.query.get_or_404(hazard_id)
    db.session.delete(hazard)
    db.session.commit()
    flash('隐患已经删除！', 'success')
    return redirect(url_for('hazard.hazard_manage'))


@hazard_bp.route('/hazard/manage', methods=['GET', 'POST'])
@login_required
def hazard_manage():
    page = request.args.get('page', 1, type=int)
    pagination = Hazard.query.order_by(Hazard.timestamp.desc()).paginate(
        page, per_page=current_app.config['HYYB_HAZARD_MANAGE_PER_PAGE'])
    hazards = pagination.items
    return render_template('hazard/hazard_manage.html', page=page, pagination=pagination, hazards=hazards)


@hazard_bp.route('/hazard/view', methods=['GET', 'POST'])
#@login_required
def hazard_view():
    page = request.args.get('page', 1, type=int)
    pagination = Hazard.query.order_by(Hazard.timestamp.desc()).paginate(
        page, per_page=current_app.config['HYYB_HAZARD_PER_PAGE'])
    hazards = pagination.items
    return render_template('hazard/hazard_view.html', page=page, pagination=pagination, hazards=hazards)
