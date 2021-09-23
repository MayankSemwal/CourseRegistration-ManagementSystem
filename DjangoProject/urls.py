"""DjangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'CRMS/', include('CRMS.urls')),

    # project 8: password
    path(r'CRMS/password_reset',
         auth_views.PasswordResetView.as_view(template_name='CRMS/reset_password.html'),
         name='password_reset'),
    path(r'CRMS/password_reset_confirm/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(template_name='CRMS/reset_password_confirm.html'),
         name='password_reset_confirm'),
    path(r'CRMS/password_reset_done',
         auth_views.PasswordResetDoneView.as_view(template_name='CRMS/reset_password_done.html'),
         name='password_reset_done'),
    path(r'CRMS/password_reset_complete',
         auth_views.PasswordResetCompleteView.as_view(template_name='CRMS/reset_password_complete.html'),
         name='password_reset_complete'),
]
