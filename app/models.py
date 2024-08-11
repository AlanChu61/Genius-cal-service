from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


# 教师表
class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    mode = Column(String, index=True)
    subjects = relationship("TeacherSubjectSalary", back_populates="teacher")
    class_records = relationship("ClassRecord", back_populates="teacher")


# 教师课时费表
class TeacherSubjectSalary(Base):
    __tablename__ = "teacher_subject_salaries"

    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    subject = Column(String, index=True)
    salary_per_hour = Column(Float, index=True)
    teacher = relationship("Teacher", back_populates="subjects")


# 学生表
class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    subject = Column(String, index=True)
    total_hours = Column(Float, index=True)
    remaining_hours = Column(Float, index=True)
    class_records = relationship("ClassRecord", back_populates="student")


# 课程记录表
class ClassRecord(Base):
    __tablename__ = "class_records"

    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    student_id = Column(Integer, ForeignKey("students.id"))
    subject = Column(String, index=True)
    date = Column(String, index=True)
    hours = Column(Float, index=True)
    teacher = relationship("Teacher", back_populates="class_records")
    student = relationship("Student", back_populates="class_records")
