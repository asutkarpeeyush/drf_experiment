from datetime import datetime
import logging
from django_cron import CronJobBase, Schedule
from django_apscheduler.jobstores import DjangoJobStore, register_events


logger = logging.getLogger(__name__)

# django_crontab
# def drf_cron():
#     log = f"I am a DRF cron. I run every minute. The current time is {datetime.now()}"
#     logger.info(log)
#     print(log)

# django_cron
# class DRFCron(CronJobBase):
#     RUN_EVERY_MINS = 1
#     schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
#     code = 'drf.django_cron'

#     def do(self):
#         log = f"I am a DRF cron. I run every minute. The current time is {datetime.now()}"
#         logger.info(log)
#         print(log)
