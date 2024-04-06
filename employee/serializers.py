from rest_framework import serializers
from .models import Attendance, User, Holiday
from datetime import datetime

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'employee_id', 'department', 'position', 'hire_date']


class AttendanceSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)

    class Meta:
        model = Attendance
        fields = ['user', 'email', 'first_name', 'last_name', 'date', 'check_in', 'check_out', 'today_tasks', 'tomorrow_tasks', 'today_tasks_status']
        read_only_fields = ['user', 'email', 'first_name', 'last_name', 'date', 'check_in', 'check_out','today_tasks', 'tomorrow_tasks', 'today_tasks_status']

class HolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Holiday
        fields = ['date', 'name']


