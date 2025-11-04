from ..models import models
from ..database.db import SessionLocal

def find_substitute(absent_teacher_id, subject, department, date_str):
    db = SessionLocal()
    try:
        # Level 1: same dept & same subject
        candidates = db.query(models.Teacher).filter(models.Teacher.department==department).all()
        for c in candidates:
            if str(c.id) != str(absent_teacher_id) and c.subjects and subject in c.subjects.split(','):
                return c
        # Level 2: same dept least-loaded
        candidates = db.query(models.Teacher).filter(models.Teacher.department==department, models.Teacher.id!=absent_teacher_id).order_by(models.Teacher.monthly_assigned).all()
        if candidates:
            return candidates[0]
        # Level 3/4: any teacher with subject or least-loaded
        candidates = db.query(models.Teacher).filter(models.Teacher.id!=absent_teacher_id).all()
        return candidates[0] if candidates else None
    finally:
        db.close()
