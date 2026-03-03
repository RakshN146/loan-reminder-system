from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from database import SessionLocal
from services.loan_status_service import update_all_loan_statuses
import os
from datetime import timezone
import pytz

scheduler = BackgroundScheduler()

def run_status_job():
    db = SessionLocal()
    try:
        updated = update_all_loan_statuses(db)
        print(f"[Scheduler] Updated {updated} loans")
    finally:
        db.close()

def start_scheduler():
    mode = os.getenv("SCHEDULER_MODE", "DAILY")

    if mode == "TEST":
        scheduler.add_job(
            run_status_job,
            IntervalTrigger(minutes=1),
            id="loan_status_test",
            replace_existing=True,
        )
        print("Scheduler running in TEST mode (every 1 minute)")

    else:
        hour = int(os.getenv("SCHEDULER_HOUR", 9))
        minute = int(os.getenv("SCHEDULER_MINUTE", 30))

        ist = pytz.timezone("Asia/Kolkata")

        scheduler.add_job(
            run_status_job,
            CronTrigger(hour=hour, minute=minute, timezone=ist),
            id="loan_status_daily",
            replace_existing=True,
        )
        print(f"Scheduler running DAILY at {hour}:{minute} IST")

    scheduler.start()

def shutdown_scheduler():
    scheduler.shutdown()