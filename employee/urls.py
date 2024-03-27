from . import views
from django.urls import path
from .views import UserRegistration, AttendanceListCreateAPIView, UserCheck_in, Usercheck_out , UserLogin, UserLogout,Attendance_history,UserProfileUpdate,UserList,UserHistory
app_name = 'attendance'

urlpatterns = [
    path('login/', UserLogin.as_view(), name='User_Login'),
    path('logout/', UserLogout.as_view(), name='User_logout'),
    path('check_in/', UserCheck_in.as_view(), name='UserCheck_in'),  # Adjusted import and naming
    path('check_out/', Usercheck_out.as_view(), name='Usercheck_out'),
    path('attendance_history/', Attendance_history.as_view(), name='Attendance_history'),
    path('register/', UserRegistration.as_view(), name='User_Registration'), 
    path('attendance/', AttendanceListCreateAPIView.as_view(), name='attendance'),
    path('profile_update/', UserProfileUpdate.as_view(), name='UserProfileUpdate'),
    path('user_history/<int:user_id>/', UserHistory.as_view(), name='UserHistory'),
    path('userlist/', UserList.as_view(), name='UserList')
]


   
