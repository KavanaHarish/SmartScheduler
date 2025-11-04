from apscheduler.schedulers.background import BackgroundScheduler
from . import jobs

sched = BackgroundScheduler()

def start_scheduler():
    try:
        # daily at 07:00
        sched.add_job(jobs.daily_reminders, 'cron', hour=7, minute=0)
        sched.start()
        print('Scheduler started')
    except Exception as e:
        print('Scheduler start error:', e)
