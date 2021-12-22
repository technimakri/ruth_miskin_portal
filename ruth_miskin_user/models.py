from django.contrib.auth.models import User
from django.db import models

from schools.models import School


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    dob = models.DateField(blank=True, null=True)
