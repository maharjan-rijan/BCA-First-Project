from django.urls import path
from .views import *
urlpatterns = [
    path("home",staff_home, name='staff_home'),
    path("notification",staff_notification, name='staff_notification'),
    path("markAsDone/<str:status>",staff_notification_markDone, name='staff_notification_markDone'),

    path("apply_leave",staff_apply_leave, name="staff_apply_leave"),
    path("apply_leave_save",apply_leave_save, name="apply_leave_save"),

    path("feedback",staff_feedback, name="staff_feedback"),
    path("feedback/save",staff_feedback_save, name="staff_feedback_save"),
    
    path("add-result",staff_add_result, name='staff_add_result'),

]
