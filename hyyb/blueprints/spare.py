

from flask import flash, redirect, url_for, render_template, Blueprint, current_app, \
    request
from flask_login import login_required, current_user

from hyyb.forms import SpareForm, SeekForm, OptForm
from hyyb.models import Departmentp, Spare, Opt, Seek
from hyyb.extensions import db
from sqlalchemy import func, literal_column

spare_bp = Blueprint('spare', __name__)


@spare_bp.route('/spare/new', methods=['GET', 'POST'])
@login_required
def spare_new():
    form = SpareForm()
    if form.validate_on_submit():
        departmentp = Departmentp.query.get(form.departmentp.data)
        designation = form.designation.data
        model = form.model.data
        quantity = form.quantity.data
        unit = form.unit.data
        purpose = form.purpose.data
        shelve = form.shelve.data
        rack = form.rack.data
        serialnum = form.serialnum.data
        place = form.place.data
        price = form.price.data
        othr = form.othr.data

        spare = Spare(departmentp=departmentp,
                      designation=designation,
                      model=model,
                      quantity=quantity,
                      unit=unit,
                      purpose=purpose,
                      shelve=shelve,
                      rack=rack,
                      serialnum=serialnum,
                      place=place,
                      price=price,
                      othr=othr)
        db.session.add(spare)
        db.session.commit()
        flash('创建了备件记录！', 'success')
        return redirect(url_for('spare.spare_manage'))
    return render_template('spare/spare_new.html', form=form)


@spare_bp.route('/spare/edit/<int:spare_id>', methods=['GET', 'POST'])
@login_required
def spare_edit(spare_id):
    form = SpareForm()
    spare = Spare.query.get_or_404(spare_id)
    if form.validate_on_submit():
#        spare.departmentp = Departmentp.query.get(form.departmentp.data)
        spare.departmentp = spare.departmentp
        spare.designation = form.designation.data
        spare.model = form.model.data
        spare.quantity = form.quantity.data
        spare.unit = form.unit.data
        spare.purpose = form.purpose.data
        spare.shelve = form.shelve.data
        spare.rack = form.rack.data
        spare.serialnum = form.serialnum.data
        spare.place = form.place.data
        spare.price = form.price.data
        spare.othr = form.othr.data
        db.session.commit()
        flash('修改了备件记录！', 'success')
        return redirect(url_for('spare.spare_manage'))
    form.designation.data = spare.designation
    form.model.data = spare.model
    form.quantity.data = spare.quantity
    form.unit.data = spare.unit
    form.purpose.data = spare.purpose
    form.shelve.data = spare.shelve
    form.rack.data = spare.rack
    form.serialnum.data = spare.serialnum
    form.place.data = spare.place
    form.price.data = spare.price
    form.othr.data = spare.othr
    form.departmentp.data = spare.departmentp_id
    return render_template('spare/spare_edit.html', form=form, spare=spare)


@spare_bp.route('/spare/delete/<int:spare_id>',  methods=['POST'])
@login_required
def spare_delete(spare_id):
    spare = Spare.query.get_or_404(spare_id)
    if spare.id == 1:
        flash('不能删除默认备件记录！','warning')
        return redirect(url_for('spare.spare_manage'))
    spare.delete()

   # db.session.delete(spare)
   # db.session.commit()
    flash('删除了备件记录！', 'success')
    return redirect(url_for('spare.spare_manage'))


@spare_bp.route('/spare/manage', methods=['GET', 'POST'])
@login_required
def spare_manage():
    page = request.args.get('page', 1, type=int)
    seek_form = SeekForm()
    desgination1 = ''
    if seek_form.validate_on_submit():
        desgination1 = seek_form.designation1.data
    #     flash('搜索成功！','success')
    pagination = Spare.query.order_by(Spare.departmentp_id.asc()).\
        filter(Spare.designation.like('%' + desgination1 + '%')).paginate(
        page, per_page=current_app.config['HYYB_SPARE_PER_PAGE'])
    spares = pagination.items

    if not spares:
        flash('没有找到符合条件的备件记录！', 'warning')
        return redirect(url_for('spare.spare_manage'))

    return render_template('spare/spare_manage.html',
                           page=page,
                           pagination=pagination,
                           spares=spares,
                           seek_form=seek_form)


@spare_bp.route('/spare/view', methods=['GET', 'POST'])
#@login_required
def spare_view():
    page = request.args.get('page', 1, type=int)

    seek_form = SeekForm()
    seek = Seek.query.get_or_404(1)
    if seek_form.validate_on_submit():
        seek.designation1 = seek_form.designation1.data
        page = 1
        db.session.commit()
#        flash('搜索成功！','success')

#    pagination = Spare.query.order_by(Spare.designation.asc()).paginate(
 #   page, per_page=current_app.config['HYYB_SPARE_PER_PAGE'])



    desgination1 = seek.designation1
    seek_form.designation1.data = seek.designation1
    pagination = Spare.query.order_by(Spare.departmentp_id.asc()).\
        filter(Spare.designation.like('%' + desgination1 + '%')).paginate(
        page, per_page=current_app.config['HYYB_SPARE_PER_PAGE'])
    spares = pagination.items

    if not spares:
        flash('没有找到符合条件的备件记录！', 'warning')
        seek.designation1 = ''
        db.session.commit()
        return redirect(url_for('spare.spare_view'))

    return render_template('spare/spare_view.html',
                           page=page,
                           pagination=pagination,
                           spares=spares,
                           seek_form=seek_form
                           )


@spare_bp.route('/spare/show/<int:spare_id>', methods=['GET', 'POST'])
#@login_required
def spare_show(spare_id):
    spare = Spare.query.get_or_404(spare_id)

    opt_form = OptForm()
    if opt_form.validate_on_submit():
        author = current_user.stuff.designation
        obtain = opt_form.obtain.data
        quantity = int(opt_form.quantity.data)
        othr = opt_form.othr.data
        spare_id = spare.id
        opt = Opt(author=author,
                  obtain=obtain,
                  quantity=quantity,
                  othr=othr,
                  spare_id=spare_id)
        if obtain == 1 or obtain == 2:
            if spare.quantity < quantity:
                flash('备件数量不足！', 'warning')
                return redirect(url_for('spare.spare_show', spare_id=spare_id,
                                        opt_form=opt_form))
            spare.quantity = spare.quantity - quantity
        elif obtain == 3:
            spare.quantity = spare.quantity + quantity

        db.session.add(opt)
        db.session.commit()
        flash('备件使用记录成功！', 'success')
        return redirect(url_for('spare.spare_show', spare_id=spare_id,
                                opt_form=opt_form))

    return render_template('spare/spare_show.html', spare=spare,
                           opt_form=opt_form)


@spare_bp.route('/spare/opt/show', methods=['GET', 'POST'])
def spare_opt_show():
    page = request.args.get('page', 1, type=int)
    pagination = Opt.query.order_by(Opt.timestamp.desc()).paginate(
        page, per_page=current_app.config['HYYB_OPT_PER_PAGE'])
    opts = pagination.items
    return render_template('spare/spare_opt_show.html',
                           page=page,
                           pagination=pagination,
                           opts=opts)
