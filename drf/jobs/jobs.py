from datetime import datetime

def my_job():
    log = f"I am a DRF cron. I run every minute. The current time is {datetime.now()}"
    # logger.info(log)
    print(log)