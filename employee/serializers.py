from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'employee_id', 'department', 'position', 'hire_date']


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['id', 'user', 'check_in_time', 'check_out_time', 'date']
        read_only_fields = ['id', 'user', 'check_in_time', 'check_out_time', 'date']



