from apscheduler.schedulers.background import BackgroundScheduler

from app.database import SessionLocal
from app.services.engine_service import run_signal_engine

scheduler = BackgroundScheduler()


def scheduled_signal_engine():
    db = SessionLocal()

    try:
        result = run_signal_engine(db)

        print(
            f"[SignalEngine] "
            f"Signals={result['filtered_count']} "
            f"Flows={result['flow_count']}"
        )

    finally:
        db.close()


def start_scheduler():
    scheduler.add_job(
        scheduled_signal_engine,
        trigger="interval",
        minutes=10, 
        id="signal_engine",
        replace_existing=True,
    )

    scheduler.start()