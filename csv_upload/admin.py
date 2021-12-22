from django.contrib import admin

from csv_upload.models import CSVUpload, SchoolUpload


class SchoolUploadInline(admin.TabularInline):
    can_delete = False
    model = SchoolUpload


class CSVUploadAdmin(admin.ModelAdmin):
    inlines = (SchoolUploadInline,)
    list_display = ('filename', 'time_created', 'outcome')
    date_hierarchy = 'time_created'


admin.site.register(CSVUpload, CSVUploadAdmin)
