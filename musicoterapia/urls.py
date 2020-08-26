from django.contrib import admin
from django.urls import path, include

from users.views import LoginView, LogoutView, RegisterView
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('formulario/', TemplateView.as_view(template_name='formulario.html'), name='formulario'),
    path('dashboard/', TemplateView.as_view(template_name='index.html'), name='dashboard'),
    path('teste', include('base.urls'))
]
