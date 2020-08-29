from django.urls import path

from base.views import IndexView

urlpatterns = [path('', IndexView.as_view())]
