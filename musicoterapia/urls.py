from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static, settings

from users.views import LoginView, LogoutView, RegisterView
from django.views.generic import TemplateView
from base.views import IndexView

from .settings import MEDIA_ROOT, MEDIA_URL

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('admin/', admin.site.urls),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path(
        'formulario/',
        TemplateView.as_view(template_name='formulario.html'),
        name='formulario',
    ),
    path('dashboard/', IndexView.as_view(), name='dashboard'),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)
