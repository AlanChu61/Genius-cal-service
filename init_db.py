import sys
import os
from datetime import datetime
from sqlalchemy.orm import Session
from app.database import engine
from app.models import Base, Teacher, TeacherSubjectSalary, Student, ClassRecord

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Create database tables
Base.metadata.create_all(bind=engine)


def init_db():
    db = Session(bind=engine)

    # Insert teacher data
    teacher1 = Teacher(name="Alice", mode="online")
    teacher2 = Teacher(name="Bob", mode="offline")

    db.add(teacher1)
    db.add(teacher2)
    db.commit()

    # Insert teacher subject salary data
    salary1 = TeacherSubjectSalary(
        teacher_id=teacher1.id, subject="Math", salary_per_hour=50.0
    )
    salary2 = TeacherSubjectSalary(
        teacher_id=teacher1.id, subject="Physics", salary_per_hour=60.0
    )
    salary3 = TeacherSubjectSalary(
        teacher_id=teacher2.id, subject="Math", salary_per_hour=55.0
    )

    db.add(salary1)
    db.add(salary2)
    db.add(salary3)
    db.commit()

    # Insert student data
    student1 = Student(
        name="Charlie", subject="Math", total_hours=100, remaining_hours=80
    )
    student2 = Student(
        name="Dave", subject="Physics", total_hours=100, remaining_hours=95
    )

    db.add(student1)
    db.add(student2)
    db.commit()

    # Insert class record data
    class_record1 = ClassRecord(
        teacher_id=teacher1.id,
        student_id=student1.id,
        subject="Math",
        date=datetime(2024, 7, 1),
        hours=2,
    )
    class_record2 = ClassRecord(
        teacher_id=teacher1.id,
        student_id=student2.id,
        subject="Physics",
        date=datetime(2024, 7, 2),
        hours=1,
    )
    class_record3 = ClassRecord(
        teacher_id=teacher2.id,
        student_id=student1.id,
        subject="Math",
        date=datetime(2024, 7, 3),
        hours=3,
    )

    db.add(class_record1)
    db.add(class_record2)
    db.add(class_record3)
    db.commit()

    db.close()


if __name__ == "__main__":
    init_db()
