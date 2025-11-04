from fastapi import APIRouter, HTTPException
from ..database.db import SessionLocal
from ..models import models

router = APIRouter()

@router.get('/{student_id}/timetable')
def student_timetable(student_id: str, month: int=None, year: int=None):
    db = SessionLocal()
    try:
        stu = db.query(models.Student).filter(models.Student.student_id==student_id).first()
        if not stu: raise HTTPException(404,'Student not found')
        q = db.query(models.Timetable).filter(models.Timetable.class_name.ilike(f'%{stu.department}%'), models.Timetable.section==stu.section)
        if month: q = q.filter(models.Timetable.month==month)
        return q.all()
    finally:
        db.close()
