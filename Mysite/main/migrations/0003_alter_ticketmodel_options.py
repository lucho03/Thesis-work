# Generated by Django 3.2.9 on 2022-01-20 09:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_ticketmodel_author'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ticketmodel',
            options={'permissions': (('answer_tickets', 'can answer tickets'),)},
        ),
    ]