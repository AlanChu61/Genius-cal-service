from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from typing import List
from . import models, schemas
from .database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware

# 创建所有表格
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# 启用 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 数据库会话的依赖注入
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 获取教师列表
@app.get("/teachers/", response_model=List[schemas.Teacher])
def read_teachers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(models.Teacher).offset(skip).limit(limit).all()


# 获取教师课时费列表，并包含教师姓名、科目、学生和课时费
@app.get("/teacher_rates/", response_model=List[schemas.TeacherRateDetail])
def read_teacher_rates(db: Session = Depends(get_db)):
    rates = (
        db.query(models.TeacherSubjectSalary)
        .options(joinedload(models.TeacherSubjectSalary.teacher))
        .all()
    )

    result = []
    for rate in rates:
        teacher_name = rate.teacher.name
        subject = rate.subject
        salary_per_hour = rate.salary_per_hour

        # 获取与教师关联的所有课程记录，并从中获取学生信息
        class_records = (
            db.query(models.ClassRecord)
            .filter_by(teacher_id=rate.teacher_id, subject=rate.subject)
            .all()
        )
        for record in class_records:
            student_name = record.student.name
            result.append(
                {
                    "teacher_name": teacher_name,
                    "subject": subject,
                    "student_name": student_name,
                    "salary_per_hour": salary_per_hour,
                }
            )

    return result


# 添加教师课时费
@app.post("/teacher_rates/", response_model=schemas.TeacherSubjectSalary)
def create_teacher_rate(
    rate: schemas.TeacherSubjectSalaryCreate, db: Session = Depends(get_db)
):
    db_rate = models.TeacherSubjectSalary(**rate.dict())
    db.add(db_rate)
    db.commit()
    db.refresh(db_rate)
    return db_rate


# 获取学生列表
@app.get("/students/", response_model=List[schemas.Student])
def read_students(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(models.Student).offset(skip).limit(limit).all()


# 获取课程记录列表
@app.get("/class_records/", response_model=List[schemas.ClassRecord])
def read_class_records(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(models.ClassRecord).offset(skip).limit(limit).all()
