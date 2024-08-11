import sqlite3
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Base, Teacher, TeacherSubjectSalary, Student, ClassRecord

# 创建数据库表
Base.metadata.create_all(bind=engine)


def init_db():
    # 连接到 data.db 文件
    data_conn = sqlite3.connect("data.db")
    data_cursor = data_conn.cursor()

    # 创建当前数据库会话
    db = SessionLocal()

    try:
        # 读取教师数据并插入到新的数据库中
        data_cursor.execute("SELECT name, mode FROM teachers")
        teachers = data_cursor.fetchall()
        for name, mode in teachers:
            teacher = Teacher(name=name, mode=mode)
            db.add(teacher)
        db.commit()

        # 获取所有教师以匹配 teacher_id
        db_teachers = db.query(Teacher).all()

        # 读取教师课时费数据并插入到新的数据库中
        data_cursor.execute(
            "SELECT teacher_id, subject, salary_per_hour FROM teacher_subject_salaries"
        )
        salaries = data_cursor.fetchall()
        for teacher_id, subject, salary_per_hour in salaries:
            # 找到对应的 teacher
            teacher = next(t for t in db_teachers if t.id == teacher_id)
            salary = TeacherSubjectSalary(
                teacher_id=teacher.id, subject=subject, salary_per_hour=salary_per_hour
            )
            db.add(salary)
        db.commit()

        # 读取学生数据并插入到新的数据库中
        data_cursor.execute(
            "SELECT name, subject, total_hours, remaining_hours FROM students"
        )
        students = data_cursor.fetchall()
        for name, subject, total_hours, remaining_hours in students:
            student = Student(
                name=name,
                subject=subject,
                total_hours=total_hours,
                remaining_hours=remaining_hours,
            )
            db.add(student)
        db.commit()

        # 读取课程记录数据并插入到新的数据库中
        data_cursor.execute(
            "SELECT teacher_id, student_id, subject, date, hours FROM class_records"
        )
        class_records = data_cursor.fetchall()
        for teacher_id, student_id, subject, date, hours in class_records:
            class_record = ClassRecord(
                teacher_id=teacher_id,
                student_id=student_id,
                subject=subject,
                date=date,
                hours=hours,
            )
            db.add(class_record)
        db.commit()

    finally:
        # 关闭数据库会话和 data.db 连接
        db.close()
        data_conn.close()


if __name__ == "__main__":
    init_db()
