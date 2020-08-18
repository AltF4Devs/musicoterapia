from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView as DjangoLoginView, LogoutView as DjangoLogoutView


login_page = 'base.html'
logout_page = ''


class LoginView(DjangoLoginView):
    template_name = login_page


class LogoutView(DjangoLogoutView):
    template_name = logout_page

