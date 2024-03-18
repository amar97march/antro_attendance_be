from . import views
from django.urls import path, include
from .views import UserRegistration, AttendanceListCreateAPIView, check_in, check_out
from .views import *
from .views import LoginAPIView

app_name = 'attendance'

urlpatterns = [
    path('api/login/', LoginAPIView.as_view(), name='login'),
    path('check-in/', check_in, name='check_in'),
    path('check-out/', check_out, name='check_out'),
    path('attendance-history/', views.attendance_history, name='attendance_history'),
    path('register/', UserRegistration.as_view(), name='register'),
    path('attendance/', AttendanceListCreateAPIView.as_view(), name='attendance'),
]


   
