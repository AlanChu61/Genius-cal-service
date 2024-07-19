from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"message": "Welcome to the Teacher Salary Management System"}


@app.post("/teachers/", response_model=schemas.Teacher)
def create_teacher(teacher: schemas.TeacherCreate, db: Session = Depends(get_db)):
    db_teacher = models.Teacher(name=teacher.name, mode=teacher.mode)
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher


@app.get("/teachers/", response_model=List[schemas.Teacher])
def read_teachers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    teachers = db.query(models.Teacher).offset(skip).limit(limit).all()
    return teachers


@app.post("/teacher_subject_salaries/", response_model=schemas.TeacherSubjectSalary)
def create_teacher_subject_salary(
    salary: schemas.TeacherSubjectSalaryCreate, db: Session = Depends(get_db)
):
    db_salary = models.TeacherSubjectSalary(
        teacher_id=salary.teacher_id,
        subject=salary.subject,
        salary_per_hour=salary.salary_per_hour,
    )
    db.add(db_salary)
    db.commit()
    db.refresh(db_salary)
    return db_salary


@app.get(
    "/teacher_subject_salaries/", response_model=List[schemas.TeacherSubjectSalary]
)
def read_teacher_subject_salaries(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    salaries = db.query(models.TeacherSubjectSalary).offset(skip).limit(limit).all()
    return salaries


@app.post("/students/", response_model=schemas.Student)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_student = models.Student(
        name=student.name,
        subject=student.subject,
        total_hours=student.total_hours,
        remaining_hours=student.remaining_hours,
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


@app.get("/students/", response_model=List[schemas.Student])
def read_students(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    students = db.query(models.Student).offset(skip).limit(limit).all()
    return students


@app.post("/class_records/", response_model=schemas.ClassRecord)
def create_class_record(
    class_record: schemas.ClassRecordCreate, db: Session = Depends(get_db)
):
    db_class_record = models.ClassRecord(
        teacher_id=class_record.teacher_id,
        student_id=class_record.student_id,
        subject=class_record.subject,
        date=class_record.date,
        hours=class_record.hours,
    )
    db.add(db_class_record)
    db.commit()
    db.refresh(db_class_record)
    # 更新学生的剩余课时
    student = (
        db.query(models.Student)
        .filter(models.Student.id == class_record.student_id)
        .first()
    )
    student.remaining_hours -= class_record.hours
    db.commit()
    return db_class_record


@app.get("/class_records/", response_model=List[schemas.ClassRecord])
def read_class_records(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    class_records = db.query(models.ClassRecord).offset(skip).limit(limit).all()
    return class_records
