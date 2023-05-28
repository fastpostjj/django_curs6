# Generated by Django 4.2.1 on 2023-05-28 20:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0006_alter_mailing_user_message_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailing',
            name='start_day',
            field=models.DateField(default='2001-01-01', verbose_name='Дата начала рассылки'),
        ),
        migrations.AlterField(
            model_name='mailing',
            name='user_message',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mailing.usermessage', verbose_name='Сообщение'),
        ),
    ]
