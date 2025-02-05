import schedule
import time
import threading
from core.log.logger import logger
from datetime import datetime

def scheduled_task():
    logger.info("Scheduled task started at " + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    try:
        # TODO: Add your scheduled task logic here
        logger.info("Scheduled task completed at " + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    except Exception as e:
        logger.error(f"Error in scheduled task: {e}")

def schedule_runner():
    """Continuously run the scheduler in a separate thread."""
    schedule.every().monday.at("04:00").do(scheduled_task)  # Run every Monday at 4 AM

    while True:
        schedule.run_pending()  # Run any scheduled tasks
        time.sleep(30)  # Check every 30 seconds to reduce CPU usage

def start_scheduler():
    """Start the scheduler in a separate thread."""
    scheduler_thread = threading.Thread(target=schedule_runner, daemon=True)
    scheduler_thread.start()
    logger.info("Background Scheduler Started")