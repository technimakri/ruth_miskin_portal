# Generated by Django 3.2.10 on 2021-12-22 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('csv_upload', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='schoolupload',
            old_name='outcome',
            new_name='error',
        ),
        migrations.AddField(
            model_name='csvupload',
            name='outcome',
            field=models.CharField(default='Pending', max_length=400),
        ),
    ]
