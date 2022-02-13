# Generated by Django 3.2.9 on 2022-02-09 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_ticketmodel_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticketmodel',
            name='status',
            field=models.CharField(choices=[('N', 'New'), ('O', 'Open'), ('P', 'Pending'), ('R', 'Resolved'), ('C', 'Closed')], default='N', max_length=1),
        ),
    ]
