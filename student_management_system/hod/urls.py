from django.urls import path
from .views import *
urlpatterns = [
path("home", home, name='hod_home'),
path("student/add", add_student, name='hod_add_student'),
path("student/view", view_student, name='hod_view_student'),
path("student/edit/<str:id>", edit_student, name='hod_edit_student'),
path("student/update", update_student, name='hod_update_student'),
path("student/delete/<str:admin>",delete_student, name='hod_delete_student'),

path("staff/add", add_staff, name='hod_add_staff'),
path("staff/view",view_staff, name='hod_view_staff'),
path("staff/edit/<str:id>",edit_staff, name='hod_edit_staff'),
path("staff/update",update_staff, name='hod_update_staff'),
path("staff/delete/<str:admin>",delete_staff, name='hod_delete_staff'),

path("course/add",add_course, name='hod_add_course'),
path("course/view",view_course, name='hod_view_course'),
path("course/edit/<str:id>",edit_course, name='hod_edit_course'),
path("course/update",update_course, name='hod_update_course'),
path("course/delete/<str:id>",delete_course, name='hod_delete_course'),

path("subject/add",add_subject, name='hod_add_subject'),
path("subject/view",view_subject, name='hod_view_subject'),
path("subject/edit/<str:id>",edit_subject, name='hod_edit_subject'),
path("subject/update",update_subject, name='hod_update_subject'),
path("subject/delete/<str:id>",delete_subject, name='hod_delete_subject'),

path("session/add",add_session, name='hod_add_session'),
path("session/view",view_session, name='hod_view_session'),
path("session/edit/<str:id>",edit_session, name='hod_edit_session'),
path("session/update",update_session, name='hod_update_session'),
path("session/delete/<str:id>",delete_session, name='hod_delete_session'),

path("staff/send_notification",staff_send_notification, name='staff_send_notification'),
path("staff/save_notification",staff_save_notification, name="staff_save_notification"),

path("student/send_notification",student_send_notification, name='student_send_notification'),
path("student/save_notification",student_save_notification, name="student_save_notification"),

path("staff/leave_view", staff_leave_view, name='staff_leave_view'),
path("staff/approve_leave/<str:id>",staff_approve_leave, name='staff_approve_leave'),
path("staff/disapprove_leave/<str:id>",staff_disapprove_leave, name='staff_disapprove_leave'),

path("student/leave_view",student_leave_view, name='student_leave_view'),
path("student/approve_leave/<str:id>",student_approve_leave, name='student_approve_leave'),
path("student/disapprove_leave/<str:id>",student_disapprove_leave, name='student_disapprove_leave'),

path("staff/feedback",staff_feedback, name="staff_feedback_reply"),
path("staff/feedback_save",staff_feedback_save, name="staff_feedback_reply_save"),

path("student/feedback",student_feedback, name="student_feedback_reply"),
path("student/feedback_save",student_feedback_save, name="student_feedback_reply_save"),
    ]