"""ruth_miskin_portal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from csv_upload.views import UploadView
from ruth_miskin_user.views import HomeView, CreateAccount

urlpatterns = [
    path('', HomeView.as_view()),
    path('accounts/create/', CreateAccount.as_view()),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/csv_upload/csvupload/add/', UploadView.as_view()),
    path('admin/', admin.site.urls)
]
