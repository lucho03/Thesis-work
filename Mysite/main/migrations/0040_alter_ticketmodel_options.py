# Generated by Django 3.2.9 on 2022-05-15 20:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0039_auto_20220321_2131'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ticketmodel',
            options={'permissions': (('create_tickets', 'can create tickets'), ('answer_tickets', 'can answer tickets'))},
        ),
    ]