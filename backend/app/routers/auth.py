from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..database.db import SessionLocal
from ..models import models
from jose import jwt
import os

router = APIRouter()
SECRET_KEY = os.getenv('SECRET_KEY','devsecret')
ALGORITHM = 'HS256'

class LoginIn(BaseModel):
    username: str
    password: str

@router.post('/login')
def login(data: LoginIn):
    db = SessionLocal()
    try:
        # Simple mock: admin login uses ADMIN_PASSWORD from env, teacher uses teacher_id, student uses student_id
        if data.username == 'admin':
            if data.password == os.getenv('ADMIN_PASSWORD','adminpass'):
                token = jwt.encode({'sub':'admin','role':'admin'}, SECRET_KEY, algorithm=ALGORITHM)
                return {'access_token': token, 'role':'admin'}
            raise HTTPException(status_code=401, detail='Invalid credentials')
        # teacher
        t = db.query(models.Teacher).filter(models.Teacher.teacher_id==data.username).first()
        if t:
            token = jwt.encode({'sub': str(t.id), 'role':'teacher'}, SECRET_KEY, algorithm=ALGORITHM)
            return {'access_token': token, 'role':'teacher', 'refId': t.id}
        s = db.query(models.Student).filter(models.Student.student_id==data.username).first()
        if s:
            token = jwt.encode({'sub': str(s.id), 'role':'student'}, SECRET_KEY, algorithm=ALGORITHM)
            return {'access_token': token, 'role':'student', 'refId': s.id}
        raise HTTPException(status_code=401, detail='Invalid credentials')
    finally:
        db.close()
