from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from ..database.db import SessionLocal, init_db
from ..models import models
from ..services import scheduler_service, notification_service
from jose import jwt
import os

router = APIRouter()

@router.post('/initdb')
def init():
    init_db()
    return {'ok': True}

class TeacherIn(BaseModel):
    name: str
    teacher_id: str
    department: str
    phone: str = None
    subjects: list = []

class StudentIn(BaseModel):
    name: str
    student_id: str
    department: str
    section: str = 'A'
    phone: str = None

@router.post('/teacher')
def create_teacher(ti: TeacherIn):
    db = SessionLocal()
    try:
        t = models.Teacher(name=ti.name, teacher_id=ti.teacher_id, department=ti.department, phone=ti.phone, subjects=','.join(ti.subjects))
        db.add(t); db.commit(); db.refresh(t)
        return t
    finally:
        db.close()

@router.post('/student')
def create_student(si: StudentIn):
    db = SessionLocal()
    try:
        s = models.Student(name=si.name, student_id=si.student_id, department=si.department, section=si.section, phone=si.phone)
        db.add(s); db.commit(); db.refresh(s)
        return s
    finally:
        db.close()

@router.post('/generate-intelligent')
def generate(payload: dict):
    year = payload.get('year'); month = payload.get('month'); classes = payload.get('classes', [])
    created = scheduler_service.generate_monthly_timetable(year, month, classes, payload.get('rooms'))
    return {'generated': len(created)}



# Holiday management endpoints
from fastapi import Query

@router.get('/holidays')
def list_holidays():
    db = SessionLocal()
    try:
        return db.query(models.Holiday).all()
    finally:
        db.close()

@router.post('/add-holiday')
def add_holiday(payload: dict):
    # payload: { "date": "YYYY-MM-DD", "description": "Desc" }
    db = SessionLocal()
    try:
        date = payload.get('date')
        desc = payload.get('description') or 'Holiday'
        if not date:
            raise HTTPException(status_code=400, detail='date required')
        # avoid duplicate
        existing = db.query(models.Holiday).filter(models.Holiday.date==date).first()
        if existing:
            return {'ok': True, 'message': 'Already exists', 'holiday': existing}
        h = models.Holiday(date=date, description=desc)
        db.add(h); db.commit(); db.refresh(h)
        return {'ok': True, 'holiday': h}
    finally:
        db.close()

@router.delete('/remove-holiday/{holiday_date}')
def remove_holiday(holiday_date: str):
    db = SessionLocal()
    try:
        del_count = db.query(models.Holiday).filter(models.Holiday.date==holiday_date).delete()
        db.commit()
        return {'ok': True, 'deleted': del_count}
    finally:
        db.close()
