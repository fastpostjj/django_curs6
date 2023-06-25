# Generated by Django 4.2.1 on 2023-06-22 19:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='client',
            options={'ordering': ('name',), 'permissions': {('set_client_status', 'can change client status')}, 'verbose_name': 'Клиент', 'verbose_name_plural': 'Клиенты'},
        ),
        migrations.AlterModelOptions(
            name='mailing',
            options={'ordering': ('is_active', 'time', 'period', 'status'), 'permissions': {('set_mailing_status', 'can change mailing status')}, 'verbose_name': 'Рассылка', 'verbose_name_plural': 'Рассылки'},
        ),
    ]