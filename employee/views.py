from rest_framework import generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User  # Import User model
from django.shortcuts import get_object_or_404
from .models import Attendance
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .serializers import AttendanceSerializer



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
        token, _ = Token.objects.get_or_create(user=user)  # Use Token
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)


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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def check_in(request):
    serializer = AttendanceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def check_out(request):
    try:
        attendance = Attendance.objects.get(user=request.user, check_out_time=None)
    except Attendance.DoesNotExist:
        return Response({"error": "No check-in found for the user"}, status=status.HTTP_400_BAD_REQUEST)

    attendance.check_out()
    serializer = AttendanceSerializer(attendance)
    return Response(serializer.data)


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






