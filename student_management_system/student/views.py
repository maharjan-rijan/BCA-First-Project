from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from main.models import *

@login_required(login_url='/')
def student_home(request):
    student = Student.objects.get(admin=request.user.id)
    subjects = Subject.objects.filter(course = student.course_id)
    context = {
        'student': student,
        'student_subject': subjects,
    }
        
    return render(request, 'STUDENT/home.html', context)

@login_required(login_url='/')
def student_notification(request):
    student = Student.objects.filter(admin=request.user.id)
    for i in student:
        student_id = i.id
        student_notification = Student_Notification.objects.filter(student_id=student_id)

        context = {'student_notification': student_notification}
    return render(request, 'STUDENT/notification.html',context)

@login_required(login_url='/')
def student_notification_markDone(request, status):
    student_notification = Student_Notification.objects.get(id=status)
    student_notification.status = 1
    student_notification.save()
    return redirect('student_notification')

@login_required(login_url='/')
def student_feedback(request):
    student_id = Student.objects.get(admin=request.user.id)
    feedback_history = Student_feedback.objects.filter(student_id=student_id)
    context = {'feedback_history': feedback_history}
    return render(request, 'STUDENT/feedback.html',context)

@login_required(login_url='/')
def student_feedback_save(request):
    if request.method == 'POST':
        feedback_message = request.POST.get('feedback_message')
        student = Student.objects.get(admin=request.user.id)
        feedback = Student_feedback(
            student_id = student,
            feedback = feedback_message,
            feedback_reply = "",
        )
        feedback.save()
        return redirect('student_feedback')
    
@login_required(login_url='/')
def student_apply_leave(request):
    student = Student.objects.filter(admin=request.user)
    for i in student:
        student_id = i.id
        student_leave_history = Student_leave.objects.filter(student_id=student_id)

        context = {'student_leave_history': student_leave_history}
    return render(request, 'STUDENT/apply_leave.html', context)

@login_required(login_url='/')
def student_apply_leave_save(request):
    if request.method == "POST":
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')

        student = Student.objects.get(admin=request.user.id)
        leave = Student_leave(
            student_id=student,
            leave_date=leave_date,
            message=leave_message,
        )
        leave.save()
        messages.success(request, 'Leave has been send successfully.')
        return redirect('student_apply_leave')
    return render(request, 'STUDENT/apply_leave.html')

@login_required(login_url='/')
def student_view_result(request):
    mark = 0
    student = Student.objects.get(admin=request.user.id)
    result = Student_Result.objects.filter(student_id=student)
    for i in result:
        assignment_marks = i.assignment_marks
        exam_marks = i.exam_mark
        mark = assignment_marks + exam_marks
    context = {
        'result': result,
        'mark': mark,
    }
    return render(request, 'STUDENT/view_result.html', context)