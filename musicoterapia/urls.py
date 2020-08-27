from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static, settings

from users.views import LoginView, LogoutView, RegisterView
from django.views.generic import TemplateView
from base.views import IndexView

from .settings import MEDIA_ROOT, MEDIA_URL

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('formulario/', TemplateView.as_view(template_name='formulario.html'), name='formulario'),
    path('dashboard/', TemplateView.as_view(template_name='index.html'), name='dashboard'),
    path('', IndexView.as_view(), name='home')
] + static(MEDIA_URL, document_root=MEDIA_ROOT)
