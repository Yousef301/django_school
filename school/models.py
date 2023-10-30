from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, DATE, Table
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, scoped_session

engine = create_engine("mysql://root:yousefQ1@localhost:3306/uni")
session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()

StudentCourse = Table(
    "student_course",
    Base.metadata,
    Column("studentID", ForeignKey('student.studentID'), primary_key=True),
    Column("courseID", ForeignKey('course.courseID'), primary_key=True),
)


class School(Base):
    __tablename__ = 'school'

    schoolID = Column("schoolID", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"{self.name}"


class Student(Base):
    __tablename__ = 'student'

    studentID = Column("studentID", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String(50))
    dob = Column("dob", DATE)
    school = Column(Integer, ForeignKey('school.schoolID'))
    schools = relationship('School', backref='students')
    courses = relationship('Course', secondary='student_course', backref='students')

    def __init__(self, name, dob, school):
        self.name = name
        self.dob = dob
        self.school = school

    def __repr__(self):
        return f"{self.name} {self.dob} {self.school}"


class Course(Base):
    __tablename__ = 'course'

    courseID = Column("courseID", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"{self.name}"


Base.metadata.create_all(engine)
