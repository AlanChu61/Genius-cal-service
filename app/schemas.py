from typing import List, Optional
from pydantic import BaseModel


class TeacherSubjectSalaryBase(BaseModel):
    subject: str
    salary_per_hour: float


class TeacherSubjectSalaryCreate(TeacherSubjectSalaryBase):
    teacher_id: int


class TeacherSubjectSalary(TeacherSubjectSalaryBase):
    id: int
    teacher_id: int

    class Config:
        orm_mode = True


class ClassRecordBase(BaseModel):
    teacher_id: int
    student_id: int
    subject: str
    date: str
    hours: float


class ClassRecordCreate(ClassRecordBase):
    pass


class ClassRecord(ClassRecordBase):
    id: int

    class Config:
        orm_mode = True


class StudentBase(BaseModel):
    name: str
    subject: str
    total_hours: float
    remaining_hours: float


class StudentCreate(StudentBase):
    pass


class Student(StudentBase):
    id: int
    class_records: List[ClassRecord] = []

    class Config:
        orm_mode = True


class TeacherBase(BaseModel):
    name: str
    mode: str


class TeacherCreate(TeacherBase):
    pass


class Teacher(TeacherBase):
    id: int
    subjects: List[TeacherSubjectSalary] = []
    class_records: List[ClassRecord] = []

    class Config:
        orm_mode = True
