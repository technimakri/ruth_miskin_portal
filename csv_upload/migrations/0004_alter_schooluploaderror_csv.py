# Generated by Django 3.2.10 on 2021-12-22 09:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('csv_upload', '0003_rename_schoolupload_schooluploaderror'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schooluploaderror',
            name='csv',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='school_errors', to='csv_upload.csvupload'),
        ),
    ]
