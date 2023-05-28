from datetime import datetime
from django.utils import timezone
from smtplib import SMTPException
from django.core.mail import send_mail, get_connection
from django.core import mail

from django.core.management import BaseCommand

from config.settings import EMAIL_HOST_USER
from mailing.models import Client, Mailing, MailingAttempts, UserMessage


class Command(BaseCommand):
    def send_email(self, subject, message_body, email):
        self.server_answer = ""
        self.status = 'successfully'
        try:
            # print("subject=", subject, "\nmessage_body=", message_body, "\nemail=", email, '\n\n')

            # send_mail(
            #         subject,
            #         message_body,
            #         EMAIL_HOST_USER,
            #         [email],
            #         # reply_to=[email],
            #         fail_silently=False,
            #         )

            with mail.get_connection() as connection:
                email_send = mail.EmailMessage(
                    subject,
                    message_body,
                    EMAIL_HOST_USER,
                    [email],
                    connection=connection,
                    # reply_to=[email],
                    # fail_silently=False,
                )
                email_send.send()
                # response = connection.send_messages([email_send])
                # print("response=", response)

        except SMTPException as error:
            self.server_answer = error
            # response = connection.send_messages([email_send])
            print("Ошибка: ", self.server_answer)
            self.status = 'unsuccessfully'
        finally:
            pass

            # получаем ответ сервера
            # connection = get_connection()
            # connection.open()
            # response = connection.send_messages([message_body])
            # connection.close()
        return self.status

    def handle(self, *args, **options):

        my_mailings = Mailing.objects.filter(is_active=True, status='run').order_by('id')

        for mailing in my_mailings:
            datetime_now =  timezone.now()
            # mailing.time
            subject = mailing.user_message.title
            message_body = mailing.user_message.text
            client_list = Client.objects.filter(is_active=True).order_by('id')
            for client in client_list:
                email = client.email
                name = client.name
                message_body = f'Уважаемый(ая), {name}!\n{message_body}'+'<a href="{{unsubscribe_link}}">Отписаться</a>'
                self.send_email(subject, message_body, email)
                # response, status = "test", "test"
                print("subject=", subject, ", message_body =", message_body, ", email=", email)

                print("email=", email, " mailing=", mailing, " datetime_now=", datetime_now, " server_answer=", self.server_answer, " status=", self.status)
                mailing_attempt = MailingAttempts(mayling=mailing, mailing_daytime=datetime_now, server_answer=self.server_answer, status=self.status, is_active=True)
                mailing_attempt.save()
