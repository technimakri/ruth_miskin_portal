from django.db import models
from django.utils import timezone


class CSVUpload(models.Model):
    class Meta:
        app_label = 'csv_upload'

    filename = models.CharField(max_length=200)
    time_created = models.DateTimeField(default=timezone.now)
    outcome = models.CharField(max_length=400, default='Processing incomplete')


class SchoolUploadError(models.Model):
    name = models.CharField(max_length=200)
    csv = models.ForeignKey(CSVUpload, on_delete=models.CASCADE, related_name='school_errors')
    error = models.CharField(max_length=400)
