from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from main.models import *


@login_required(login_url='/')
def staff_home(request):
    return render(request, 'STAFF/home.html')

@login_required(login_url='/')
def staff_notification(request):
    staff = Staff.objects.filter(admin=request.user.id)
    for i in staff:
        staff_id = i.id
        staff_notification = Staff_Notification.objects.filter(staff_id=staff_id)

        context = {'staff_notification': staff_notification}
    return render(request, 'STAFF/notification.html', context)

@login_required(login_url='/')
def staff_notification_markDone(request, status):
    staff_notification = Staff_Notification.objects.get(id=status)
    staff_notification.status = 1
    staff_notification.save()
    return redirect('staff_notification')

@login_required(login_url='/')
def staff_apply_leave(request):
    staff = Staff.objects.filter(admin=request.user)
    for i in staff:
        staff_id = i.id
        staff_leave_history = Staff_leave.objects.filter(staff_id=staff_id)

        context = {'staff_leave_history': staff_leave_history}
    return render(request, 'STAFF/apply_leave.html', context)

@login_required(login_url='/')
def apply_leave_save(request):
    if request.method == "POST":
        leaave_date = request.POST.get('leaave_date')
        leave_message = request.POST.get('leave_message')

        staff = Staff.objects.get(admin=request.user.id)
        leave = Staff_leave(
            staff_id = staff,
            leave_date = leaave_date,
            message = leave_message,
        )
        leave.save()
        messages.success(request, 'Leave has been send successfully.')
        return redirect('staff_apply_leave')

@login_required(login_url='/')
def staff_feedback(request):
    staff_id = Staff.objects.get(admin=request.user.id)
    feedback_history = Staff_feedback.objects.filter(staff_id=staff_id)
    context = {'feedback_history': feedback_history}
    return render(request, 'STAFF/feedback.html',context)

@login_required(login_url='/')
def staff_feedback_save(request):
    if request.method == "POST":
        feedback_message = request.POST.get('feedback_message')
        staff = Staff.objects.get(admin=request.user.id)
        feedback = Staff_feedback(
            staff_id = staff,
            feedback = feedback_message,
            feedback_reply = "",
        )
        feedback.save()
        return redirect('staff_feedback')
    
   