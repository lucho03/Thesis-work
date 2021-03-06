# Generated by Django 3.2.9 on 2022-01-27 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_answermodel'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ticketmodel',
            old_name='priorities',
            new_name='priority',
        ),
        migrations.AddField(
            model_name='ticketmodel',
            name='status',
            field=models.CharField(choices=[('O', 'Open'), ('P', 'Pending'), ('R', 'Resolved'), ('C', 'Closed')], default='O', max_length=1),
        ),
    ]
