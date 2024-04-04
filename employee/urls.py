from . import views
from django.urls import path
from .views import UserRegistration, AttendanceListCreateAPIView, UserCheck_in, UserCheck_Out,UserLogin, UserLogout,TodayAttendance,HolidayListView
app_name = 'attendance'

urlpatterns = [
    path('login/', UserLogin.as_view(), name='User_Login'),
    #path('logout/', UserLogout.as_view(), name='User_logout'),
    path('check_in/', UserCheck_in.as_view(), name='UserCheck_in'),  # Adjusted import and naming
    path('check-out/', UserCheck_Out.as_view(), name='check_out'),
    path('today_details/', TodayAttendance.as_view(), name='today_details'),
    path('attendance-history/', views.attendance_history, name='attendance_history'),
    path('holidays/<int:year>/', HolidayListView.as_view(), name='holiday-list'),
    path('register/', UserRegistration.as_view(), name='User_Registration'),
    path('attendance/', AttendanceListCreateAPIView.as_view(), name='attendance'),
]


   
