from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from main.models import *


@login_required(login_url='/')
def staff_home(request):
    staff = Staff.objects.filter(admin=request.user.id)
    for i in staff:
        staff_id = i.id 
        staff_subject = Subject.objects.filter(staff_id=staff_id)
        
        context = {'staff_subject' : staff_subject}
    return render(request, 'STAFF/home.html', context)

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
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')

        staff = Staff.objects.get(admin=request.user.id)
        leave = Staff_leave(
            staff_id = staff,
            leave_date = leave_date,
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
    
   # ===================================Result==================================== #
@login_required(login_url='/')
def staff_add_result(request):
    staff = Staff.objects.get(admin=request.user.id)
    subject = Subject.objects.filter(staff_id = staff)
    session_year = Session_year.objects.all()
    action = request.GET.get('action')
    get_subject = None
    get_session_year = None
    students = None
    
    if action is not None:
        if request.method == "POST":
            subject_id = request.POST.get('subject_id')
            session_year_id = request.POST.get('session_year_id')
            
            get_subject = Subject.objects.get(id=subject_id)
            get_session_year = Session_year.objects.get(id=session_year_id)
            
            subjects = Subject.objects.filter(id=subject_id)
            for i in subjects:
                student_id = i.course.id
                students = Student.objects.filter(course_id=student_id)
    context = {
        'subject': subject,
        'session_year': session_year,
        'action': action,
        'get_subject': get_subject,
        'get_session': get_session_year,
        'students': students,
    }   
    return render(request,'Staff/add_result.html', context)

@login_required(login_url='/')
def staff_save_result(request):
    if request.method == "POST":
        subject_id = request.POST.get('subject_id')
        student_id = request.POST.get('student_id')
        assignment_marks = request.POST.get('assignment_marks')
        exam_mark = request.POST.get('exam_mark')

        get_student = Student.objects.get(admin=int(student_id))
        get_subject = Subject.objects.get(id=subject_id)  
              
        check_exists = Student_Result.objects.filter(subject_id=get_subject, student_id=get_student).exists()
        if check_exists:
            result = Student_Result.objects.get(subject_id=get_subject, student_id=get_student)
            result.assignment_marks = assignment_marks
            result.exam_mark = exam_mark
            result.save()
            messages.success(request, "Result updated successfully")
            return redirect('staff_add_result')
        else:
            result = Student_Result(
                student_id = get_student,
                subject_id = get_subject,
                assignment_marks = assignment_marks,
                exam_mark = exam_mark,
            )
            result.save()
            messages.success(request, "Result added successfully")
            return redirect('staff_add_result')
        

@login_required(login_url='/')
def staff_take_attendance(request):
    staff_id = Staff.objects.get(admin = request.user.id)
    subject = Subject.objects.filter(staff = staff_id)
    session_year = Session_year.objects.all()
    action = request.GET.get('action')
    
    get_subject = None
    get_session_year = None
    students = None
    
    if action is not None:
        if request.method == "POST":
            subject_id = request.POST.get('subject_id')
            session_year_id = request.POST.get('session_year_id')
            
            get_subject = Subject.objects.get(id = subject_id)
            get_session_year = Session_year.objects.get(id = session_year_id)
            
            subjects = Subject.objects.filter(id = subject_id)
            for i in subjects:
                student_id = i.course.id
                students = Student.objects.filter(course_id=student_id)
    context = {
        'subject': subject,
        'session_year': session_year,
        'action': action,
        'get_subject': get_subject,
        'get_session': get_session_year,
        'students': students,
    }   
    return render(request, 'Staff/take_attendance.html', context)

@login_required(login_url='/')
def staff_save_attendance(request):
    if request.method == "POST":
        subject_id = request.POST.get('subject_id')
        session_year_id = request.POST.get('session_year_id')
        attendance_date = request.POST.get('attendance_date')
        student_id = request.POST.getlist('student_id')
        
        get_subject = Subject.objects.get(id=subject_id)
        get_session_year = Session_year.objects.get(id=session_year_id)
        
        attendance = Attendance(
            subject_id = get_subject,
            attendance_date = attendance_date,
            session_year_id = get_session_year
        )
        attendance.save()
        for i in student_id:
            stud_id = i
            int_stud = int(stud_id)
            
            p_students = Student.objects.get(id = int_stud)
            attendance_report = AtendanceReport(
                student_id = p_students,
                attendance_id = attendance,
            )
            attendance_report.save()
            return redirect('staff_take_attendance')     
        
@login_required(login_url='/')
def staff_view_attendance(request):
    staff_id = Staff.objects.get(admin = request.user.id)
    subject = Subject.objects.filter(staff = staff_id)
    session_year = Session_year.objects.all()
    
    context = {
        'subject': subject,
        'session_year': session_year,
    }   
    return render(request, 'Staff/view_attendance.html', context)    