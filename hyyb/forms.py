# -*- coding: utf-8 -*-
"""
Created on Wed Apr  9 07:35:55 2025

@author: Administrator
"""
from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, ValidationError, HiddenField, \
    BooleanField, PasswordField, IntegerField, DateField, FloatField, DateTimeField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, Email, Length, Optional, URL, NumberRange

from hyyb.models import Department, Departmentp, Jobcategory, Stuff


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('密码', validators=[DataRequired(), Length(1, 128)])
    remember = BooleanField('Remember me')
    
    submit = SubmitField('登录')


class SettingForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired(), Length(1, 60)])
    othr = StringField('其他', validators=[DataRequired(), Length(1, 60)])

    submit = SubmitField()


class StuffForm(FlaskForm):
    num = IntegerField('工号', validators=[DataRequired(), NumberRange(1, 5000)])
    designation = StringField('姓名', validators=[DataRequired(), Length(1, 20)])
    gendar = BooleanField('性别', default=False)
    dcome = DateField('上班日期', validators=[DataRequired()])   #
    school = StringField('毕业学校', validators=[DataRequired(), Length(1, 60)])
    degree = StringField('学历', validators=[DataRequired(), Length(1, 20)])
    phone = StringField('电话', validators=[DataRequired(), Length(1, 20)])
    addr = StringField('地址', validators=[DataRequired(), Length(1, 100)])
    department = StringField('车间', validators=[DataRequired(), Length(1, 20)])
    team = IntegerField('班组', validators=[DataRequired(), NumberRange(1, 4)])
    situation = StringField('状态', validators=[DataRequired(), Length(1, 20)])
    manage = BooleanField('管理人员', default=False)
    othr = StringField('其他', validators=[DataRequired(), Length(1, 60)])
    
    submit = SubmitField()


class AttendanceForm(FlaskForm):
    stuff = SelectField('员工', coerce=int, default=1)   #
    datestamp = DateField('日期', validators=[DataRequired()])   #
    am = BooleanField('上午')
    pm = BooleanField('下午')
    trip = BooleanField('公差')
    othr = StringField('其他', validators=[DataRequired(), Length(1, 60)])
    
    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        super(AttendanceForm, self).__init__(*args, **kwargs)
        self.stuff.choices = [(stuff.id, stuff.designation)
                              for stuff in Stuff.query.order_by(Stuff.designation).all()]


class HazardForm(FlaskForm):
    department = SelectField('车间', coerce=int, default=1)   #
    content = CKEditorField('内容', validators=[DataRequired()])
    material = CKEditorField('材料备件', validators=[DataRequired()])
    material_ok = BooleanField('材料准备完成')
    director = StringField('材料备件负责人', validators=[DataRequired(), Length(1, 20)])
    cooperators = StringField('协作人员', validators=[DataRequired(), Length(1, 100)])
    scheme = CKEditorField('方案', validators=[DataRequired()])
    leader = StringField('负责人', validators=[DataRequired(), Length(1, 20)])
    othr = StringField('其他', validators=[DataRequired(), Length(1, 60)])
    onstop = BooleanField('需停车')
    
    submit = SubmitField()
    
    def __init__(self, *args, **kwargs):
        super(HazardForm, self).__init__(*args, **kwargs)
        self.department.choices = [(department.id, department.designation)
                                 for department in Department.query.order_by(Department.designation).all()]


class DepartmentForm(FlaskForm):
    designation = StringField('名称', validators=[DataRequired(), Length(1, 20)])
    othr = StringField('其他', validators=[DataRequired(), Length(1, 60)])
   
    submit = SubmitField()


class SpareForm(FlaskForm):
    departmentp = SelectField('仓库', coerce=int)   #
    designation = StringField('名称', validators=[DataRequired(), Length(1, 80)])
    model = StringField('型号', validators=[DataRequired(), Length(1, 80)])
    quantity = IntegerField('数量', validators=[DataRequired(), NumberRange(1, 500)])
    unit = StringField('单位', validators=[DataRequired(), Length(1, 20)])
    purpose = StringField('用途', validators=[DataRequired(), Length(1, 60)])
    shelve = IntegerField('货架', validators=[DataRequired(), NumberRange(1, 50)])
    rack = IntegerField('架层', validators=[DataRequired(), NumberRange(1, 50)])
    serialnum = IntegerField('序号', validators=[DataRequired(), NumberRange(1, 50)])
    place = StringField('位置', validators=[DataRequired(), Length(1, 60)])
    price = FloatField('单价')
    othr = StringField('其他', validators=[DataRequired(), Length(1, 60)])
    
    submit = SubmitField()
    
    def __init__(self, *args, **kwargs):
        super(SpareForm, self).__init__(*args, **kwargs)
        self.departmentp.choices = [(departmentp.id, departmentp.designation)
                              for departmentp in Departmentp.query.order_by(Departmentp.designation).all()]


class DepartmentpForm(FlaskForm):
    designation = StringField('名称', validators=[DataRequired(), Length(1, 20)])
    othr = StringField('其他', validators=[DataRequired(), Length(1, 60)])
   
    submit = SubmitField()


class DiaryForm(FlaskForm):
    worker = StringField('作业人', validators=[DataRequired(), Length(1, 20)])
    start_time = DateTimeField('起始时间', validators=[DataRequired()])
    end_time = DateTimeField('结束时间', validators=[DataRequired()])
    content = CKEditorField('内容', validators=[DataRequired()])
    jobcategory = SelectField('工作分类', coerce=int, default=1)   #
    auditor = StringField('确认人', validators=[DataRequired(), Length(1, 20)])
    datestamp = StringField('Datestamp', validators=[DataRequired()])
    factor = FloatField('系数', validators=[DataRequired(), NumberRange(0.1, 10.0)])
    othr = StringField('其他', validators=[DataRequired(), Length(1, 60)])
    
    submit = SubmitField()
    
    def __init__(self, *args, **kwargs):
        super(DiaryForm, self).__init__(*args, **kwargs)
        self.jobcategory.choices = [(jobcategory.id, jobcategory.designation)
                                 for jobcategory in Jobcategory.query.order_by(Jobcategory.designation).all()]


class JobcategoryForm(FlaskForm):
    designation = StringField('工作名称', validators=[DataRequired(), Length(1, 20)])
    score = FloatField('分数', validators=[DataRequired(), NumberRange(0.5, 30.0)])
    othr = StringField('其他', validators=[DataRequired(), Length(1, 60)])
   
    submit = SubmitField()


class MessageForm(FlaskForm):
    designation = StringField('名称', validators=[DataRequired(), Length(1, 20)])
    body = TextAreaField('消息内容', validators=[DataRequired()])
    othr = StringField('其他', validators=[DataRequired(), Length(1, 60)])
    
    submit = SubmitField()


class LinkForm(FlaskForm):
    designation = StringField('名称', validators=[DataRequired(), Length(1, 30)])
    url = StringField('URL', validators=[DataRequired(), URL(), Length(1, 255)])
    
    submit = SubmitField()


class SeekForm(FlaskForm):
    clear = SubmitField()
    selector0 = SelectField('搜索', choices=[(1, '备件'), (2, '人员'), (3, '仓库')], default='1', coerce=int)
    designation1 = StringField('名称1', default='')
    designation2 = StringField('名称2', default='')
    designation3 = StringField('名称3', default='')
    designation4 = StringField('名称4', default='')
    submit = SubmitField()


class OptForm(FlaskForm):
    author = HiddenField()
    quantity = IntegerField('数量', validators=[DataRequired(), NumberRange(1, 500)])
    obtain = SelectField('存取', choices=[(1, '取用'),(2, '报废'),  (3, '存回')], default='1', coerce=int)
    othr = StringField('其他', validators=[DataRequired(), Length(1, 60)])

    submit = SubmitField()

# upload form
class UploadForm(FlaskForm):
    doc = FileField('Upload excel', validators=[FileRequired(['xlsx'])])

    submit = SubmitField()