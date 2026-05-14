from django.urls import path, re_path
from . import views
from .views import MyUserView

urlpatterns = [re_path(r'^(?P<id_key>[^/]+)/api/$', MyUserView.as_view()),
               path("", views.index, name="index"),
               ]
# http://myservice.com/...... /17/api/ -> MyUserView
