from django.urls import path
from . import views

urlpatterns = [
    # 다른 URL 패턴들...
    
    # fortune_view 추가
    path('fortune/', views.fortune_view, name='fortune_view'),
]
