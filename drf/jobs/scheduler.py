from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from .jobs import my_job

def start_scheduler():
  scheduler = BackgroundScheduler()
  # scheduler = BlockingScheduler()
  scheduler.add_job(my_job, 'interval', seconds=3)
  scheduler.start()
  print("Background schdeuler started")
