from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'employee_id', 'department', 'position', 'hire_date']


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['user', 'date','check_in', 'check_out', 'tasks']
        read_only_fields = [ 'user','date', 'check_in', 'check_out', 'tasks']



