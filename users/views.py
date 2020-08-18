from django.shortcuts import render
from django.contrib.auth.views import LoginView as DjangoLoginView, LogoutView as DjangoLogoutView


login_page = 'login.html'
logout_page = ''


class LoginView(DjangoLoginView):
    template_name = login_page


class LogoutView(DjangoLogoutView):
    template_name = logout_page

