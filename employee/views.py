from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Attendance
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .serializers import AttendanceSerializer
from django.contrib.auth import authenticate
from .serializers import UserSerializer
from rest_framework.authtoken.models import Token  # Import Token model
from rest_framework_simplejwt.views import TokenViewBase
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User
import json
from rest_framework_simplejwt.settings import api_settings
from datetime import datetime, date
from rest_framework import status
from .models import Holiday
from .serializers import HolidaySerializer
from rest_framework import generics
import holidays
from datetime import datetime, timedelta
from .models import Attendance, User
from django.utils import timezone
from datetime import datetime







class AttendanceListCreateAPIView(generics.ListCreateAPIView):
    """
    API view to list all attendance records or create a new attendance record.
    """
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AttendanceDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update or delete a specific attendance record.
    """
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    lookup_field = 'id'

class UserRegistration(APIView):
    def post(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            emp_id = request.data.get('emp_id')
            if not email or not password:
                return Response({'error': 'email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

            if User.objects.filter(email=email).exists():
                return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.create(email=email, employee_id = emp_id)
            user.set_password(password)
            user.save()
            data =  {
                'status': 200,
                'messsge': "User registered"
            }
            # print(Token,"Token")
            # token, created = Token.objects.get_or_create(user=user)  # Corrected usage of Token.objects.get_or_create
            return Response(data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return JsonResponse({'message': 'User not registered'}, status=400)


class UserAttendanceListAPIView(APIView):
    """
    API view to list all attendance records for a specific user.
    """
    def get(self, request, user_id):
        attendances = Attendance.objects.filter(user_id=user_id)
        serializer = AttendanceSerializer(attendances, many=True)
        return Response(serializer.data)


class UserAttendanceDetailAPIView(APIView):
    """
    API view to retrieve, update or delete a specific attendance record for a user.
    """
    def get(self, request, user_id, attendance_id):
        attendance = get_object_or_404(Attendance, id=attendance_id, user_id=user_id)
        serializer = AttendanceSerializer(attendance)
        return Response(serializer.data)

    def put(self, request, user_id, attendance_id):
        attendance = get_object_or_404(Attendance, id=attendance_id, user_id=user_id)
        serializer = AttendanceSerializer(attendance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id, attendance_id):
        attendance = get_object_or_404(Attendance, id=attendance_id, user_id=user_id)
        attendance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserCheck_in(APIView):
    permission_classes = [IsAuthenticated,]

    def post(self, request):
        user = request.user
        user_obj = User.objects.get(id=request.user.id)
        today_date = date.today()  # Get the current date
        yesterday_date = today_date - timedelta(days=1)  # Get yesterday's date

        # Fetch today's tasks based on yesterday's date
        today_tasks = Attendance.objects.filter(user=user_obj, date=yesterday_date).values_list('tomorrow_tasks', flat=True).first()

        # If there are no tasks from yesterday, set today's tasks to an empty string
        if today_tasks is None:
            today_tasks = ''

        # Check if the user has already checked in today
        check_in_object = Attendance.objects.filter(user=user_obj, date=today_date).first()

        if check_in_object and check_in_object.check_out == None:
            return Response({"status": 200, "message": "Already checked in"}, status=status.HTTP_200_OK)
        elif check_in_object and check_in_object.check_out:
            return Response({"status": 200, "message": "Already checked out"}, status=status.HTTP_200_OK)
        else:
            # Create a new Attendance object for check-in
            Attendance.objects.create(user=user, date=today_date, check_in=datetime.now(), tomorrow_tasks=today_tasks)
            return Response({"status": 200, "message": "Check-in successful", "today_tasks": today_tasks}, status=status.HTTP_200_OK)
class SummaryAverageHours(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.query_params.get('user_id')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if not all([user_id, start_date, end_date]):
            return Response({"error": "Missing required parameters"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD"}, status=status.HTTP_400_BAD_REQUEST)

        check_ins = Attendance.objects.filter(user=user, date__range=[start_date, end_date], check_out__isnull=False)

        total_hours = sum((check_out - check_in).seconds / 3600 for check_in, check_out in check_ins.values_list('check_in', 'check_out'))
        num_days = (end_date - start_date).days + 1
        average_hours_per_day = total_hours / num_days if num_days > 0 else 0

        return Response({
            "status": 200,
            "message": "Summary of average hours worked for the specified date range",
            "average_hours_per_day": average_hours_per_day
        }, status=status.HTTP_200_OK)
    



class UserCheck_Out(APIView):
    """
    API view to handle user check-out.
    """
    def post(self, request):
        """
        Handle user check-out.
        """
        user = request.user
        today_date = datetime.now().date()
        today_tasks = request.data.get('today_tasks')  # Fix the variable name here
        tomorrow_tasks = request.data.get('tomorrow_tasks')
        today_tasks_status = request.data.get('today_tasks_status')

        if not all([today_tasks, tomorrow_tasks, today_tasks_status]):
            return Response({'error': 'Fields cannot be empty'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Check if there's an existing check-in for today
            attendance_obj = Attendance.objects.filter(user=user, date=today_date, check_in__isnull=False).first()
            if attendance_obj:
                if attendance_obj.check_out:
                    return Response({'error': 'Already checked out'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    # Update attendance details
                    attendance_obj.today_tasks = today_tasks
                    attendance_obj.tomorrow_tasks = tomorrow_tasks
                    attendance_obj.today_tasks_status = today_tasks_status
                    attendance_obj.check_out = timezone.now()  # Save checkout time
                    attendance_obj.save()
                    return Response({"message": "Checkout successful"})
            else:
                return Response({'error': 'No check-in found for today'}, status=status.HTTP_400_BAD_REQUEST)
        except Attendance.DoesNotExist:
            return Response({'error': 'No check-in found for today'}, status=status.HTTP_400_BAD_REQUEST)

class TodayAttendance(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        user = request.user
        today_date = datetime.now().date()
        check_in_time = None
        check_out_time = None
        tasks = None
    
        try:
            check_in_object = Attendance.objects.filter(user=user, date=today_date).first()
            
            if check_in_object:
                check_in_time = check_in_object.check_in.strftime("%Y-%m-%d %H:%M:%S") if check_in_object.check_in else None
                check_out_time = check_in_object.check_out.strftime("%Y-%m-%d %H:%M:%S") if check_in_object.check_out else None
                tasks = check_in_object.tasks
        
            response_data = {
                "user": user.email,
                "date": today_date,
                "check_in_time": check_in_time,
                "check_out_time": check_out_time,
                "tasks": tasks
            }
            return Response(response_data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# holidays_api/views.py

class HolidayListView(APIView):
    def get(self, request, year):
        try:
            # Get the list of holidays for the specified year
            holiday_list = holidays.CountryHoliday('US', years=[year])
            # Serialize the holiday data
            serializer = HolidaySerializer([
                {'date': date, 'name': name} for  date , name in holiday_list.items()
            ], many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def attendance_history(request):
    attendances = Attendance.objects.filter(user=request.user)
    serializer = AttendanceSerializer(attendances, many=True)
    return Response(serializer.data)


class LoginAPIView(APIView):
     def post(self, request):
        from .serializers import UserSerializer  # Import moved here to avoid circular dependency
        serializer = TokenObtainPairSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

class UserLogin(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(username=email, password=password)
        if user is not None:
            # User is authenticated, generate token
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
            # token, created = Token.objects.get_or_create(user=user)
            # return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            # Invalid credentials
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class UserLogout(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            request.user.auth_token.delete()
        except Token.DoesNotExist:
            pass  # Token does not exist for the user, no need to delete anything
        
        return Response(status=status.HTTP_200_OK)
    

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['roles'] = user.role

        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        print('KK', data)
        refresh = self.get_token(self.user)

        # Add extra responses here
        data['email'] = self.user.email
        data['roles'] = self.user.role
        # data['roles'] = self.user.role
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


"""class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
"""
class TokenRefreshView(TokenViewBase):
    """
    Takes a refresh type JSON web token and returns an access type JSON web
    token if the refresh token is valid.
    """

    _serializer_class = api_settings.TOKEN_REFRESH_SERIALIZER


token_refresh = TokenRefreshView.as_view()


@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        try:
            user = User.objects.get(username=username, password=password)
            return JsonResponse({'message': 'Login successful'})
        except User.DoesNotExist:
            return JsonResponse({'message': 'Invalid credentials'}, status=400)
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)



    