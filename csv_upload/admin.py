from django.contrib import admin

from csv_upload.models import CSVUpload, SchoolUploadError


class SchoolUploadErrorInline(admin.TabularInline):
    can_delete = False
    model = SchoolUploadError


class CSVUploadAdmin(admin.ModelAdmin):
    inlines = (SchoolUploadErrorInline,)
    list_display = ('filename', 'time_created', 'outcome')
    date_hierarchy = 'time_created'


admin.site.register(CSVUpload, CSVUploadAdmin)
