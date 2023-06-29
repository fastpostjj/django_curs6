# Generated by Django 4.2.1 on 2023-06-26 20:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mailing', '0003_client_user_mailing_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermessage',
            name='user',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='автор'),
        ),
    ]
