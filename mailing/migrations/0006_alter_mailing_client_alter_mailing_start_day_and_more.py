# Generated by Django 4.2.1 on 2023-07-02 20:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0005_mailing_client'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailing',
            name='client',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='mailing.client', verbose_name='клиент'),
        ),
        migrations.AlterField(
            model_name='mailing',
            name='start_day',
            field=models.DateField(auto_now_add=True, verbose_name='Дата начала рассылки'),
        ),
        migrations.AlterField(
            model_name='mailing',
            name='time',
            field=models.TimeField(auto_now_add=True, verbose_name='Время начала рассылки'),
        ),
    ]
