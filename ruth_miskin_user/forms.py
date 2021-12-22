from django.forms import ModelForm, ModelChoiceField

from ruth_miskin_user.models import Teacher
from schools.models import School


class TeacherForm(ModelForm):
    school = ModelChoiceField(queryset=School.objects.filter(open=True).order_by('school_name'))

    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'email', 'dob']
        labels = {
            'dob': ('Date of birth'),
        }
        help_texts = {
            'dob': ('Please use the format DD/MM/YYYY e.g. 10/05/1991'),
        }
