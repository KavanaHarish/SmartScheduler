from fastapi import APIRouter, HTTPException, Depends
from ..database.db import SessionLocal
from ..models import models
from ..services import substitute_service, notification_service
from pydantic import BaseModel

router = APIRouter()

@router.get('/pending/{teacher_id}')
def get_pending(teacher_id: int, month: int=None, year: int=None):
    db = SessionLocal()
    try:
        q = db.query(models.Timetable).filter(models.Timetable.teacher_id==teacher_id)
        if month: q = q.filter(models.Timetable.month==month)
        return q.all()
    finally:
        db.close()

class ResponseIn(BaseModel):
    response: str

@router.patch('/respond/{entry_id}')
def respond(entry_id: int, body: ResponseIn):
    db = SessionLocal()
    try:
        entry = db.query(models.Timetable).get(entry_id)
        if not entry: raise HTTPException(404,'Not found')
        entry.teacher_response = body.response
        db.add(entry); db.commit()
        if body.response == 'unavailable':
            # run substitute logic for this entry
            sub = substitute_service.find_substitute(entry.teacher_id, entry.subject, entry.class_name, entry.date)
            if sub:
                entry.teacher_id = sub.id
                entry.auto_assigned = True
                entry.status = 'substituted'
                db.add(entry); db.commit()
                # notify substitute and students
                if sub.phone:
                    notification_service.send_sms(sub.phone, f'You are assigned as substitute for {entry.class_name} on {entry.date} ({entry.subject})')
                # students
                studs = db.query(models.Student).filter(models.Student.department==entry.class_name).all()
                nums = [s.phone for s in studs if s.phone]
                if nums:
                    notification_service.send_bulk_sms(nums, f'Update: {entry.class_name} {entry.section} - {entry.subject} on {entry.date} will be taken by {sub.name}')
        return {'ok': True, 'entry': entry}
    finally:
        db.close()
