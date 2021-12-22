from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.views import View

from ruth_miskin_user.forms import TeacherForm


class HomeView(View):

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, 'ruth_miskin_user/home.html', context=context)


class CreateAccount(View):

    def get(self, request, *args, **kwargs):
        user_form = UserCreationForm()
        teacher_form = TeacherForm()
        context = {'user_form': user_form, 'teacher_form': teacher_form}

        return render(request, 'ruth_miskin_user/create_account.html', context=context)
