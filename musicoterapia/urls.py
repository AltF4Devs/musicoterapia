from django.contrib import admin
from django.urls import path, include
from django.urls import path

from base import urls
from users.views import LoginView, LogoutView, RegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('teste', include('base.urls'))
]
