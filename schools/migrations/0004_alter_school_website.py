# Generated by Django 3.2.10 on 2021-12-22 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0003_auto_20211222_0929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='website',
            field=models.URLField(blank=True, max_length=400, null=True),
        ),
    ]
