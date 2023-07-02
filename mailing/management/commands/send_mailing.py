from datetime import datetime, timedelta
from django.utils import timezone
from smtplib import SMTPException
from django.core import mail
from django.core.management import BaseCommand
from config.settings import EMAIL_HOST_USER
from mailing.models import Client, Mailing, MailingAttempts, UserMessage
from mailing.services.send_mailing import find_malling_for_send

class Command(BaseCommand):
    def handle(self, *args, **options):
        find_malling_for_send()
