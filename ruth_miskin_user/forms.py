from django.forms import ModelForm, ModelChoiceField, DateField

from ruth_miskin_user.models import Teacher
from schools.models import School


class TeacherForm(ModelForm):
    school = ModelChoiceField(queryset=School.objects.filter(open=True).order_by('school_name'))
    dob = DateField(input_formats=['%d/%m/%Y'], label='Date of birth',
                    help_text='Please use the format DD/MM/YYYY e.g. 10/05/1991. This field is not mandatory.')

    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'email']
