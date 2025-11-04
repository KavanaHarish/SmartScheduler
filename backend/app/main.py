from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, admin, teacher, student
from .core import scheduler as scheduler_core

app = FastAPI(title='HackNova SmartScheduler')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(auth.router, prefix='/api/auth')
app.include_router(admin.router, prefix='/api/admin')
app.include_router(teacher.router, prefix='/api/teacher')
app.include_router(student.router, prefix='/api/student')

@app.on_event('startup')
async def startup_event():
    # start scheduled jobs (daily reminders)
    scheduler_core.start_scheduler()
