from . import views
from django.urls import path
from .views import UserRegistration, AttendanceListCreateAPIView, UserCheck_in, UserLogin, UserLogout

app_name = 'attendance'

urlpatterns = [
    path('login/', UserLogin.as_view(), name='User_Login'),
    path('logout/', UserLogout.as_view(), name='User_logout'),
    path('check_in/', UserCheck_in.as_view(), name='UserCheck_in'),  # Adjusted import and naming
    # path('check-out/', CheckOut.as_view(), name='check_out'),
    path('attendance-history/', views.attendance_history, name='attendance_history'),
    path('register/', UserRegistration.as_view(), name='User_Registration'),
    path('attendance/', AttendanceListCreateAPIView.as_view(), name='attendance'),
]


   
