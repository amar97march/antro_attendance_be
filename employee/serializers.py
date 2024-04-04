from rest_framework import serializers
from .models import *
from .models import Holiday

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'employee_id', 'department', 'position', 'hire_date']


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['user', 'check_in_time', 'check_out_time', 'date',"tasks"]
        read_only_fields = [ 'user', 'check_in_time', 'check_out_time', 'date',"tasks"]

class HolidaySerializer(serializers.Serializer):
    date = serializers.DateField()
    name = serializers.CharField()


