from datetime import datetime, timedelta
from django.utils import timezone
from smtplib import SMTPException
from django.core import mail
from django.core.management import BaseCommand
from config.settings import EMAIL_HOST_USER
from mailing.models import Client, Mailing, MailingAttempts, UserMessage
from mailing.services.send_mailing import find_malling_for_send

class Command(BaseCommand):
#     def send_email(self, subject, message_body, email):
#         self.server_answer = ""
#         self.status = 'successfully'
#         try:
#
#             with mail.get_connection() as connection:
#                 email_send = mail.EmailMessage(
#                     subject,
#                     message_body,
#                     EMAIL_HOST_USER,
#                     [email],
#                     connection=connection
#                 )
#                 email_send.send()
#
#         except SMTPException as error:
#             self.server_answer = error
#             self.status = 'unsuccessfully'
#         finally:
#             pass
#         return self.status
#
#     def find_malling_for_send(self, *args, **kwargs):
#         next_send_datetime = timezone.now()
#         last_send_datetime = timezone.now()
#         mailings = Mailing.objects.filter(is_active=True, status='run').order_by('id')
#         for mailing in mailings:
#             send_flug = False
#             datetime_now =  timezone.now()
#             subject = mailing.user_message.title
#             message_body = mailing.user_message.text
#             last_send = MailingAttempts.objects.filter(mayling=mailing, status = 'successfully').order_by('-mailing_daytime')
#             # print('last_send=', last_send)
#
#             if last_send:
#                 # Сообщение успешно отправлялось, находим дату и время следующей отправки
#                 last_send_datetime = list(last_send)[0].mailing_daytime #.strftime('%d-%m-%Y %H:%M')
#                 if mailing.period == 'monthly':
#                     next_send_datetime = list(last_send)[0].mailing_daytime + timedelta(days=30)
#                 elif mailing.period == 'weekly':
#                     next_send_datetime = list(last_send)[0].mailing_daytime + timedelta(days=7)
#                 else:
#                     next_send_datetime = list(last_send)[0].mailing_daytime + timedelta(days=1)
#             else:
#                 # Сообщение еще ни разу не отправлялось - ставим флаг для отправки
#                 send_flug = True
#             if next_send_datetime <= datetime_now:
#                 send_flug = True
#
#             # print('mailing=', mailing, ' send_flug=', send_flug)
#             # print('last_send_datetime=', last_send_datetime, 'next_send_datetime=', next_send_datetime)
#             # print('datetime_now=', datetime_now)
#
#             if mailing.client and send_flug:
#             # for client in client_list:
#                 email = mailing.client.email
#                 name = mailing.client.name
#                 message_body = f'Уважаемый(ая), {name}!\n{message_body}'
#                 # print('send mail')
#                 # print('mailing.client=', mailing.client, ' mailing.status=', mailing.status, ' mailing.period=', mailing.period, ' next_send_datetime=', next_send_datetime)
#                 self.send_email(subject, message_body, email)
#
#                 # print("subject=", subject, ", message_body =", message_body, ", email=", email)
#
#                 # print("email=", email, " mailing=", mailing, " datetime_now=", datetime_now, " server_answer=", self.server_answer, " status=", self.status)
#                 mailing_attempt = MailingAttempts(mayling=mailing, mailing_daytime=datetime_now, server_answer=self.server_answer, status=self.status, is_active=True)
#                 mailing_attempt.save()


    def handle(self, *args, **options):
        find_malling_for_send()
