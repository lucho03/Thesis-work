# Generated by Django 3.2.9 on 2022-01-26 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_alter_ticketmodel_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticketmodel',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
