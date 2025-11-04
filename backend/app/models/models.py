from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..database.db import Base
import datetime

class Department(Base):
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

class ClassRoom(Base):
    __tablename__ = 'classrooms'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    department = Column(String)
    section = Column(String)
    smartboard = Column(Boolean, default=False)

class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    teacher_id = Column(String, unique=True, index=True)
    department = Column(String, index=True)
    phone = Column(String)
    subjects = Column(String)  # comma separated for simplicity
    monthly_assigned = Column(Integer, default=0)

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    student_id = Column(String, unique=True, index=True)
    department = Column(String)
    section = Column(String)
    phone = Column(String)

class Timetable(Base):
    __tablename__ = 'timetable'
    id = Column(Integer, primary_key=True, index=True)
    date = Column(String, index=True)  # ISO date
    month = Column(Integer)
    year = Column(Integer)
    class_name = Column(String)
    section = Column(String)
    subject = Column(String)
    teacher_id = Column(Integer, ForeignKey('teachers.id'), nullable=True)
    room = Column(String)
    finalized = Column(Boolean, default=False)
    status = Column(String, default='pending') # pending|confirmed|substituted
    teacher_response = Column(String, nullable=True) # available|unavailable|null
    auto_assigned = Column(Boolean, default=False)
    sent_notifications = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Holiday(Base):
    __tablename__ = 'holidays'
    id = Column(Integer, primary_key=True, index=True)
    date = Column(String, unique=True, index=True)  # ISO date string YYYY-MM-DD
    description = Column(String, nullable=True)
