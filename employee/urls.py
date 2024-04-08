from . import views
from django.urls import path
from .views import UserRegistration,UserHistory, UserList, UserProfileUpdate, Attendance_history, AttendanceListCreateAPIView, UserCheck_in, UserCheck_Out,UserLogin,TodayAttendance,HolidayListView,SummaryAverageHours, UserAnalytics
app_name = 'attendance'

urlpatterns = [
    path('login/', UserLogin.as_view(), name='User_Login'),
    # path('logout/', UserLogout.as_view(), name='User_logout'),
    path('check_in/', UserCheck_in.as_view(), name='UserCheck_in'),
    path('check_out/', UserCheck_Out.as_view(), name='Usercheck_out'),
    path('attendance_history/', Attendance_history.as_view(), name='Attendance_history'),
    path('register/', UserRegistration.as_view(), name='User_Registration'), 
    # path('attendance/', AttendanceListCreateAPIView.as_view(), name='attendance'),
    path('profile_update/', UserProfileUpdate.as_view(), name='UserProfileUpdate'),
    path('user_history/<int:user_id>/', UserHistory.as_view(), name='UserHistory'),
    path('userlist/', UserList.as_view(), name='UserList'),

    # path('check-out/', UserCheck_Out.as_view(), name='check_out'),
    path('today_details/', TodayAttendance.as_view(), name='today_details'),
    # path('attendance-history/', views.attendance_history, name='attendance_history'),
    path('holidays/<int:year>/', HolidayListView.as_view(), name='holiday-list'),
    path('register/', UserRegistration.as_view(), name='User_Registration'),
    path('attendance/', AttendanceListCreateAPIView.as_view(), name='attendance'),
    path('api/summary-average-hours/', SummaryAverageHours.as_view(), name='summary-average-hours'),
    path('user_analytics/', UserAnalytics.as_view(), name='user_analytics'),
]