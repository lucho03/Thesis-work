# Generated by Django 3.2.9 on 2022-02-09 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0022_ticketmodel_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answermodel',
            name='comments',
            field=models.TextField(default='Comments'),
        ),
        migrations.AlterField(
            model_name='ticketmodel',
            name='comments',
            field=models.TextField(default='Comments'),
        ),
    ]
