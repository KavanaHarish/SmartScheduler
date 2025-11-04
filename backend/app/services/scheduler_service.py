from ..models import models
from ..database.db import SessionLocal
from datetime import date, timedelta, datetime
from ..services.notification_service import send_sms

def weekdays_in_month_excluding_holidays(year, month):
    import calendar
    db = SessionLocal()
    try:
        # fetch holiday dates as strings YYYY-MM-DD
        holidays = [h.date for h in db.query(models.Holiday).all()]
    finally:
        db.close()
    days = []
    c = calendar.Calendar()
    for d in c.itermonthdates(year, month):
        if d.month==month and d.weekday()<5:  # Mon-Fri (0-4)
            if d.strftime('%Y-%m-%d') in holidays:
                continue
            days.append(d)
    return days

def weekdays_in_month(year, month):
    # backward compatible wrapper
    return weekdays_in_month_excluding_holidays(year, month)

def generate_monthly_timetable(year, month, classes_config, rooms=None):
    db = SessionLocal()
    created = []
    try:
        days = weekdays_in_month(year, month)
        if not days:
            return created
        for cls in classes_config:
            subjects = cls.get('subjects', [])
            if not subjects:
                continue
            si = 0
            # create a circular iterator but only on working days
            for d in days:
                subj = subjects[si % len(subjects)]
                si += 1
                tt = models.Timetable(date=str(d), month=month, year=year, class_name=cls.get('class_name') or cls.get('name'), section=cls.get('section','A'), subject=subj['name'], room=(rooms[0]['name'] if rooms else 'R-101'))
                db.add(tt)
                created.append(tt)
        db.commit()
        # notify teachers (placeholder: notify all teachers)
        teachers = db.query(models.Teacher).all()
        for t in teachers:
            if t.phone:
                send_sms(t.phone, f'Preliminary timetable for {month}/{year} is ready. Visit your dashboard to review.')
        return created
    finally:
        db.close()
