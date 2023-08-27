from time import sleep
from celery import shared_task

@shared_task()
def drf_sleeping_task():
    sleep(20)