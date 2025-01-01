from time import sleep
from celery import shared_task

# @celery.task
@shared_task
def notify_customers(message):
    print('Send 10k emails')
    print(message)
    sleep(10)
    print('email sent')