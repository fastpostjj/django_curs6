# Generated by Django 4.2.1 on 2023-07-02 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0006_alter_mailing_client_alter_mailing_start_day_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailing',
            name='start_day',
            field=models.DateField(default='01:01:2001', verbose_name='Дата начала рассылки'),
        ),
        migrations.AlterField(
            model_name='mailing',
            name='time',
            field=models.TimeField(default='0:00:00', verbose_name='Время начала рассылки'),
        ),
    ]
