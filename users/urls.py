from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


app_name = 'user'

urlpatterns = [
    path("login/", views.login_view, name = 'login'),
    path("signup/", views.signup_view, name = 'signup'),
    path("logout/", views.logout_view, name="logout"),
    path("update/", views.update_view, name = "update"),
]