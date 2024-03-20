from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
# from django.contrib.auth.models import User  # Import User model
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
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password)
        refresh = RefreshToken.for_user(user)

        data =  {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        # print(Token,"Token")
        # token, created = Token.objects.get_or_create(user=user)  # Corrected usage of Token.objects.get_or_create
        return Response(data, status=status.HTTP_201_CREATED)

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


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def check_in(request):
#     data = request.data
#     data["check_in"] = datetime.now()
#     serializer = AttendanceSerializer(data=data)
#     if serializer.is_valid():
#         serializer.save(user=request.user)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserCheck_in(APIView):
    permission_classes = [IsAuthenticated,]
    def post(self, request):
        user = request.user
        print(request.user.id)
        user_obj = User.objects.get(id = request.user.id)
        today_date = date.today()  # Get the current date
        check_in_object = Attendance.objects.filter(user=user_obj, date=today_date).exclude(check_out = None).first()
        if not check_in_object:
            Attendance.objects.create(user=user, date=today_date, check_in = datetime.now())
            return Response({"status": 200, "message": "check in successful"}, status=status.HTTP_200_OK)
        else:
             return Response({"status": 400, "message": "check in unsuccessful"}, status=status.HTTP_200_OK)

       


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def attendance_history(request):
    attendances = Attendance.objects.filter(user=request.user)
    serializer = AttendanceSerializer(attendances, many=True)
    return Response(serializer.data)


"""class LoginAPIView(APIView):
    def post(self, request):
        from .serializers import UserSerializer  # Import moved here to avoid circular dependency
        serializer = TokenObtainPairSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })"""

class UserLogin(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            # User is authenticated, generate token
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            # Invalid credentials
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class UserLogout(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        request.user.auth_token.delete()
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
            return Response(status=status.HTTP_400_BAD_REQUEST)"""

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
