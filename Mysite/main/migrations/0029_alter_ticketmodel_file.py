# Generated by Django 3.2.9 on 2022-02-20 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0028_alter_ticketmodel_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticketmodel',
            name='file',
            field=models.FileField(null=True, upload_to='main/static/capture_files_folder'),
        ),
    ]