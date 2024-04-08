from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
#from django.contrib.auth.models import User
from .models import User, Attendance, AllowedIP, Holiday

# Register your models here.
admin.site.register(User)
admin.site.register(Attendance)
admin.site.register(Holiday)
admin.site.register(AllowedIP)