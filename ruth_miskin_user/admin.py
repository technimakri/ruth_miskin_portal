from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from ruth_miskin_user.models import Teacher


class TeacherInline(admin.StackedInline):
    model = Teacher
    can_delete = False


class CustomUserAdmin(UserAdmin):
    inlines = (TeacherInline,)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
