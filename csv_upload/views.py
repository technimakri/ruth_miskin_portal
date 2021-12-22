import csv

from django.core.exceptions import ValidationError
from django.core.files.uploadhandler import TemporaryFileUploadHandler
from django.forms import URLField
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.datetime_safe import datetime
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from csv_upload.forms import CSVUploadForm
from csv_upload.models import CSVUpload, SchoolUploadError
from schools.mixins import SuperUserRequiredMixin
from schools.models import School


def csv_uploader(csv_file, field_names):
    """
    Uploads the contents of a csv file containing school records to the database. Only adds 'open' schools.
     Creates a database record for the newly uploaded file and any errors that occur.
    :param csv_file: A .csv wrapped in Django's TemporaryUploadedFile wrapper.
    :param field_names: A list of field names for the csv.
    :return: The primary key of the uploaded csv file, to be used in URL construction.
    """

    def convert_date(date):
        """
        Converts a date to a datetime instance.
        :param date: Date in string format dd/mm/yyyy
        :return: Datetime instance
        """
        if date:
            return datetime.strptime(date, "%d/%m/%Y").date()
        else:
            return None

    def validate_url(url):
        """
        If given, validates a URL using Django's URLValidator.
        :param url: URL in string format.
        :return: A cleaned URL.
        """
        if url:
            url_form_field = URLField()
            url_cleaned = url_form_field.clean(url)
            return url_cleaned
        else:
            return ''

    def convert_status(status):
        """
        Converts the school status to a boolean value.
        :param status: School status in string format.
        :return: Bool.
        """
        if 'Open' in status:
            return True
        else:
            return False

    # Create new database record for uploaded file.
    csv_record = CSVUpload.objects.create(filename=csv_file.name)
    try:
        with open(csv_file.temporary_file_path(), newline='', encoding='ISO-8859-1') as csv_file:
            reader = csv.DictReader(csv_file, fieldnames=field_names)
            next(reader)  # Ignore first line of CSV containing column titles.

            for row in reader:
                if not convert_status(row['open']):  # Ignore closed schools.
                    continue
                try:
                    School.objects.create(
                        urn=row['urn'],
                        school_name=row['school_name'],
                        open=convert_status(row['open']),
                        open_date=convert_date(row['open_date']),
                        close_date=convert_date(row['close_date']),
                        town=row['town'],
                        postcode=row['postcode'],
                        website=validate_url(row['website']),
                        phone_number=row['phone_number']
                    )
                except Exception as school_error:
                    # Create new error record for schools that have invalid data.
                    SchoolUploadError.objects.create(name=row['school_name'], csv=csv_record, error=school_error)

        if csv_record.school_errors.count() > 0:
            csv_record.outcome = 'Success with some errors'
            csv_record.save()
        else:
            csv_record.outcome = 'Success'
            csv_record.save()

    except Exception as csv_error:
        csv_record.outcome = csv_error
        csv_record.save()

    return csv_record.id


# Exempt view from CSRF to set upload handler, re-protect once _post is called.
# See https://docs.djangoproject.com/en/4.0/topics/http/file-uploads/#modifying-upload-handlers-on-the-fly
@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(csrf_protect, name='_post')
class UploadView(SuperUserRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        form = CSVUploadForm()
        context = {'form': form}

        return render(request, 'csv_upload/upload.html', context=context)

    def post(self, request, *args, **kwargs):
        request.upload_handlers = [TemporaryFileUploadHandler(request)]  # Set custom upload handler before upload begins
        return self._post(request)

    def _post(self, request, *args, **kwargs):
        field_names = ['urn', 'school_name', 'open', 'open_date', 'close_date',
                       'town', 'postcode', 'website', 'phone_number']
        csv_id = csv_uploader(request.FILES['csv_file'], field_names)

        return HttpResponseRedirect(f'/admin/csv_upload/csvupload/{csv_id}')
