from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static, settings
from django.contrib.auth.views import LogoutView

from users.views import LoginView, RegisterView
from django.views.generic import TemplateView
from base.views import IndexView, FormView, CompletedFormView

from .settings import MEDIA_ROOT, MEDIA_URL

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('admin/', admin.site.urls),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('form/', FormView.as_view(), name='form'),
    path(
        'completed_form/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9',
        CompletedFormView.as_view(),
        name='completed_form',
    ),
    path('dashboard/', IndexView.as_view(), name='dashboard'),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)
