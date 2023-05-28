from management.commands import send_mail_all_clients

def my_scheduled_job():
  send_mail_all_clients()