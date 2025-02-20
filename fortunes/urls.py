from django.urls import path
from . import views

app_name = 'fortunes'

urlpatterns = [
    path("result/", views.get_fortune, name = 'get_fortune'),

]