import string

from .models import User
from django.utils.crypto import get_random_string

from celery import shared_task

@shared_task
def create_random_user_accounts(total):
    for i in range(total):
        username = 'user_{}'.format(get_random_string(10, string.ascii_letters))
        email = '{}@example.com'.format(username)
        password = get_random_string(50)
        User.objects.create_user(username=username, email=email, password=password)
    return '{} random users created with success!'.format(total)


from celery.task.schedules import crontab
from celery.decorators import periodic_task
from django.core.mail import EmailMessage

@periodic_task(run_every=crontab(minute='*/1'))
def send_mail_periodically():
    email = EmailMessage()
    email.subject = "Maze mail"
    email.body = "hello you are recieving"
    email.to = ['piyalgeorge@gmail.com',]
    email.send()