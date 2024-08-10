from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from . import models, schemas, database  # 改为相对导入

# 创建数据库表
models.Base.metadata.create_all(bind=database.engine)

# 初始化 FastAPI 应用
app = FastAPI()

# 配置 CORS
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


@app.get("/teachers/{teacher_id}", response_model=schemas.Teacher)
def read_teacher(teacher_id: int, db: Session = Depends(get_db)):
    teacher = db.query(models.Teacher).filter(models.Teacher.id == teacher_id).first()
    if teacher is None:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return teacher


@app.get("/students/", response_model=List[schemas.Student])
def read_students(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    students = db.query(models.Student).offset(skip).limit(limit).all()
    return students


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


@app.get("/students/{student_id}", response_model=schemas.Student)
def read_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@app.get("/class_records/", response_model=List[schemas.ClassRecord])
def read_class_records(
    skip: int = 0,
    limit: int = 10,
    teacher_id: Optional[int] = None,
    student_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    if teacher_id:
        class_records = (
            db.query(models.ClassRecord)
            .filter(models.ClassRecord.teacher_id == teacher_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    elif student_id:
        class_records = (
            db.query(models.ClassRecord)
            .filter(models.ClassRecord.student_id == student_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    else:
        class_records = db.query(models.ClassRecord).offset(skip).limit(limit).all()
    return class_records


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
    return db_class_record
