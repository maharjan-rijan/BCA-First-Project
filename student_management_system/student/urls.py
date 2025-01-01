from django.urls import path
from .views import *
urlpatterns = [
    path("home",student_home, name='student_home'),

    path("notification",student_notification, name='student_notification'),
    path("markAsDone/<str:status>",student_notification_markDone,name='student_notification_markDone'),

    path("feedback",student_feedback, name="student_feedback"),
    path("feedback/save",student_feedback_save, name="student_feedback_save"),

    path("apply_leave",student_apply_leave, name="student_apply_leave"),
    path("apply_leave_save",student_apply_leave_save, name="student_apply_leave_save"),
]
