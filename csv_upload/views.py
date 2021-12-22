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
from csv_upload.models import CSVUpload, SchoolUpload
from schools.models import School


def csv_uploader(csv_file, field_names):

    def convert_date(date):
        if date:
            return datetime.strptime(date, "%d/%m/%Y").date()
        else:
            return None

    def validate_url(url):
        if url:
            url_form_field = URLField()
            url_cleaned = url_form_field.clean(url)
            return url_cleaned
        else:
            return ''

    def convert_status(status):
        if 'Open' in status:
            return True
        else:
            return False

    csv_record = CSVUpload.objects.create(filename=csv_file.name)
    try:
        with open(csv_file.temporary_file_path(), newline='') as csv_file:
            reader = csv.DictReader(csv_file, fieldnames=field_names)
            next(reader)  # Ignore first line containing column titles
            for row in reader:
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
                    SchoolUpload.objects.create(name=row['school_name'], csv=csv_record, error=school_error)

        csv_record.outcome = 'Success'
        csv_record.save()

    except Exception as csv_error:
        csv_record.outcome = csv_error
        csv_record.save()

    return csv_record.id

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(csrf_protect, name='_post')
class UploadView(View):

    def get(self, request, *args, **kwargs):
        form = CSVUploadForm()
        context = {'form': form}

        return render(request, 'csv_upload/upload.html', context=context)

    def post(self, request, *args, **kwargs):
        request.upload_handlers = [TemporaryFileUploadHandler(request)]
        return self._post(request)

    def _post(self, request, *args, **kwargs):
        field_names = ['urn', 'school_name', 'open', 'open_date', 'close_date',
                       'town', 'postcode', 'website', 'phone_number']
        csv_id = csv_uploader(request.FILES['csv_file'], field_names)

        return HttpResponseRedirect(f'/admin/csv_upload/csvupload/{csv_id}')
