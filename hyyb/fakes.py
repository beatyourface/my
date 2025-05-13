import random

from faker import Faker
from sqlalchemy.exc import IntegrityError

from hyyb.extensions import db
from hyyb.models import Link, Admin, Jobcategory, Message, Departmentp, Department, \
    Stuff, Attendance, Spare, Diary, Hazard, Opt, Seek
fake = Faker('zh_CN')


def fake_links():
    twitter = Link(designation='Twitter', url='#')
    facebook = Link(designation='Facebook', url='#')
    linkedin = Link(designation='LinkedIn', url='#')
    google = Link(designation='Google+', url='#')
    db.session.add_all([twitter, facebook, linkedin, google])
    db.session.commit()


def fake_admins(count=20):
    admin = Admin(
        username='admin',
        privilege=1,
        title="No, I'm the real thing.",
        othr='默认管理员',
        stuff = Stuff.query.get(1)

    )
    admin.set_password('123456')
    db.session.add(admin)

    for i in range(count):
        admin = Admin(
            username=Stuff.query.get(i+2).designation,
            privilege=random.choice([0, 1]),
            title=fake.job(),
            othr=fake.sentence(),
            stuff = Stuff.query.get(i+2)
        )
        admin.set_password('123456')
        db.session.add(admin)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_jobcategories(count=10):
    jobcategory = Jobcategory(designation='Default',
                              score=6.5,
                              othr='默认分类')
    db.session.add(jobcategory)

    for i in range(count):
        jobcategory = Jobcategory(designation=fake.word(),
                                  score=fake.pydecimal(left_digits=2, right_digits=1, positive=True),
                                  othr=fake.sentence())
        db.session.add(jobcategory)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_messages(count=20):
    for i in range(count):
        message = Message(
            designation=fake.name(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            author=Admin.query.get(random.randint(1, Admin.query.count())).stuff.designation,
            othr=fake.sentence()
        )
        db.session.add(message)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_departmentps(count=10):
    departmentp = Departmentp(designation='Default',
                              othr='默认仓库')
    db.session.add(departmentp)
    for i in range(count):
        departmentp = Departmentp(designation=fake.word(),
                                  othr=fake.sentence())

        db.session.add(departmentp)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_departments(count=20):
    department = Department(designation='Default',
                            othr='默认车间')

    db.session.add(department)
    for i in range(count):
        department = Department(designation=fake.word(),
                                othr=fake.sentence())

        db.session.add(department)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_stuffs(count=20):
    stuff = Stuff(num=000000,
                  designation='虚拟员工',
                  gendar=True,
                  dcome=fake.date_of_birth(),
                  school=fake.company(),
                  degree=fake.job(),
                  phone=fake.phone_number(),
                  addr=fake.address(),
                  team=random.randint(1, 10),
                  situation='在职',
                  manage=False,
                  othr=fake.sentence(),
                  department=Department.query.get(1)
                  )
    db.session.add(stuff)

    for i in range(count):
        stuff = Stuff(num=random.randint(100000, 999999),
                      designation=fake.name(),
                      gendar=random.choice([True, False]),
                      dcome=fake.date_of_birth(),
                      school=fake.company(),
                      degree=fake.job(),
                      phone=fake.phone_number(),
                      addr=fake.address(),
                      team=random.randint(1, 10),
                      situation=random.choice(['在职', '离职']),
                      manage=random.choice([True, False]),
                      othr=fake.sentence(),
                      department=Department.query.get(random.randint(1, Department.query.count()))
                      )

        db.session.add(stuff)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_attendances(count=20):
    for i in range(count):
        attendance = Attendance(datestamp=fake.date_time_this_year(),
                                am=random.choice([True, False]),
                                pm=random.choice([True, False]),
                                trip=random.choice([True, False]),
                                othr=fake.sentence(),
                                stuff=Stuff.query.get(random.randint(1, Stuff.query.count()))
                                )
        db.session.add(attendance)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_hazards(count=20):
    for i in range(count):
        hazard = Hazard(timestamp=fake.date_time_this_year(),
                        content=fake.sentence(),
                        material=fake.sentence(),
                        material_ok=random.choice([True, False]),
                        director=fake.name(),
                        cooperators=fake.name(),
                        scheme=fake.sentence(),
                        leader=fake.name(),
                        othr=fake.sentence(),
                        onstop=random.choice([True, False]),
                        department=Department.query.get(random.randint(1, Department.query.count()))
                        )

        db.session.add(hazard)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_diaries(count=20):
    for i in range(count):
        diary = Diary(start_time=fake.date_time_this_year(),
                      end_time=fake.date_time_this_year(),
                      worker=fake.name(),
                      content=fake.sentence(),
                      auditor=fake.name(),
                      datestamp=fake.date_time_this_year(),
                      factor=fake.pydecimal(left_digits=2, right_digits=1, positive=True),
                      othr=fake.sentence(),
                      jobcategory=Jobcategory.query.get(random.randint(1, Jobcategory.query.count()))
                      )

        db.session.add(diary)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_spares(count=20):
    for i in range(count):
        spare = Spare(designation=fake.word(),
                      model=fake.word(),
                      quantity=random.randint(1, 100),
                      unit=fake.word(),
                      purpose=fake.word(),
                      shelve=random.randint(1, 50),
                      rack=random.randint(1, 10),
                      serialnum=random.randint(1, 50),
                      place=fake.word(),
                      price=fake.pydecimal(left_digits=2, right_digits=1, positive=True),
                      othr=fake.sentence(),
                      departmentp=Departmentp.query.get(random.randint(1, Departmentp.query.count()))
                      )

        db.session.add(spare)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_opts(count=40):
    for i in range(count):
        opt = Opt(  timestamp=fake.date_time_this_year(),
                    author=fake.name(),
                    quantity=random.randint(1, 100),
                    obtain=random.choice([1, 2, 3]),
                    othr=fake.sentence(),
                    spare=Spare.query.get(random.randint(1, Spare.query.count()))
                    )
    db.session.add(opt)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()

def fake_seek():
    seek = Seek(
        designation1='',
        designation2='',
        designation3='',
        designation4=''
    )
    db.session.add(seek)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()