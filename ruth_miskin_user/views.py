from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from ruth_miskin_user.forms import TeacherForm
from ruth_miskin_user.models import Teacher


class HomeView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'ruth_miskin_user/home.html')


class CreateAccount(View):

    def get(self, request, *args, **kwargs):
        user_form = UserCreationForm(prefix='user_creation')
        teacher_form = TeacherForm(prefix='teacher_creation')
        context = {'user_form': user_form, 'teacher_form': teacher_form}

        return render(request, 'ruth_miskin_user/create_account.html', context=context)

    def post(self, request, *args, **kwargs):
        # Add prefixes to separate request data.
        user_form = UserCreationForm(request.POST, prefix='user_creation')
        teacher_form = TeacherForm(request.POST, prefix='teacher_creation')

        if user_form.is_valid() and teacher_form.is_valid():
            # Create temporary user and teacher model.
            new_user = user_form.save(commit=False)
            new_teacher = Teacher(**teacher_form.cleaned_data)
            new_teacher.user = new_user  # Add user model as Teacher model's user foreign key
            new_user.save()
            new_teacher.save()

            return HttpResponseRedirect('/accounts/login')

        # If forms not valid, re-render form with errors shown.
        context = {'user_form': user_form, 'teacher_form': teacher_form}
        return render(request, 'ruth_miskin_user/create_account.html', context=context)
