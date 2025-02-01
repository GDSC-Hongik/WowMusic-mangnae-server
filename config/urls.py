"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
<<<<<<< HEAD
from django.urls import path, include
from users import views


#router = routers.DefaultRouter() # viewset 자동으로 url 연결
#router.register('users', UserViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    #path('api/', include(router.urls)),
=======
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
>>>>>>> 0fc62c8ad1934d93d225b5bc4804ffd2d5bc5abf
]
