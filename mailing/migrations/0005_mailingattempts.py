# Generated by Django 4.2.1 on 2023-05-27 20:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0004_mailing_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='MailingAttempts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mailing_daytime', models.DateTimeField(blank=True, null=True, verbose_name='Дата и время последней попытки')),
                ('server_answer', models.CharField(blank=True, max_length=200, null=True, verbose_name='Ответ почтового сервера')),
                ('status', models.CharField(blank=True, choices=[('successfully', 'успешно'), ('unsuccessfully', 'неудачно')], max_length=14, null=True, verbose_name='Статус рассылки')),
                ('is_active', models.BooleanField(default=True, verbose_name='активная')),
                ('mayling', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mailing.mailing')),
            ],
            options={
                'verbose_name': 'Попытка рассылки',
                'verbose_name_plural': 'Попытки рассылки',
                'ordering': ('mailing_daytime', 'server_answer'),
            },
        ),
    ]
