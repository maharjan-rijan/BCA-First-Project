from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
# Register your models here.
class UserModel(UserAdmin):
    list_display = ['username', 'user_type','first_name', 'last_name', 'email']

admin.site.register(CustomUser, UserModel)
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Staff)
admin.site.register(Subject)
admin.site.register(Staff_Notification)
admin.site.register(Student_Notification)
admin.site.register(Staff_leave)
admin.site.register(Student_leave)
admin.site.register(Staff_feedback)
admin.site.register(Student_feedback)
admin.site.register(Attendance)
admin.site.register(AttendanceReport)
admin.site.register(Student_Result)