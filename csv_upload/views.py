from django.shortcuts import render
from django.views import View

from csv_upload.forms import CSVUploadForm

def csv_uploader(csv_file):
    pass


class UploadView(View):

    def get(self, request, *args, **kwargs):
        form = CSVUploadForm()
        context = {'form': form}
        return render(request, 'csv_upload/upload.html', context=context)

    def post(self, request, *args, **kwargs):
        csv_uploader(request.FILES['csv_file'])
