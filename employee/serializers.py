from rest_framework import serializers
from .models import *
from datetime import datetime

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.
    
    Includes additional fields for profile update.
    """
    # Add additional fields for profile update
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    department = serializers.CharField(required=False)
    position = serializers.CharField(required=False)
    hire_date = serializers.DateField(required=False)
    hometown = serializers.CharField(required = False)
    qualification = serializers.CharField(required = False)
    hobbies = serializers.CharField(required = False)
    image = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'employee_id', 'department', 'position', 'hire_date']
        fields = ['email', 'first_name', 'last_name', 'employee_id', 'department', 'position', 'hire_date','hometown','qualification','hobbies','image']

    def update(self, instance, validated_data):

        """
        Updates user profile fields.
        """
        # Update profile fields
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.department = validated_data.get('department', instance.department)
        instance.position = validated_data.get('position', instance.position)
        instance.hire_date = validated_data.get('hire_date', instance.hire_date)
        instance.hometown = validated_data.get('hometown', instance.hometown)
        instance.qualification = validated_data.get('qualification', instance.qualification)
        instance.hobbies = validated_data.get('hobbies', instance.hobbies)
        instance.image = validated_data.get('image', instance.image)

        # Save the instance
        instance.save()
        return instance

class AttendanceSerializer(serializers.ModelSerializer):
    """
    Serializer for Attendance model.
    """
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)

    class Meta:
        model = Attendance
        fields = ['user','email', 'first_name','last_name','date','check_in', 'check_out', 'todays_tasks','tomorrow_tasks','today_tasks_status']
        read_only_fields = [ 'user','email', 'first_name','last_name','date', 'check_in', 'check_out', 'todays_tasks','tomorrow_tasks','today_tasks_status']
    def create(self, validated_data):
        validated_data['check_out'] = datetime.now()  # Set default check_out time
        return super().create(validated_data)

class UserListSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying user details in the user list.
    """
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)

    class Meta:
        model = Attendance
        fields = ['user', 'email', 'first_name', 'last_name']