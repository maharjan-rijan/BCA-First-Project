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
    academic_years = Student.objects.values_list('academic_year', flat=True).distinct()
    action = request.GET.get('action')
    get_subject = None
    get_academic_year = None
    students = Student.objects.none()
    
    if action and request.method == "POST":
        subject_id = request.POST.get('subject_id')
        get_academic_year = request.POST.get('academic_year')
            
        if subject_id and get_academic_year:
            get_subject = Subject.objects.get(id=subject_id)
            students = Student.objects.select_related('admin').filter(course_id=get_subject.course_id, academic_year=get_academic_year)
    context = {
        'subject': subject,
        'action': action,
        'get_subject': get_subject,
        'get_academic_year': get_academic_year,
        'academic_years': academic_years,
        'students': students,
    }   
    return render(request,'Staff/add_result.html', context)

@login_required(login_url='/')
def staff_save_result(request):
    if request.method != "POST":
        return redirect('staff_add_result')

    subject_id = request.POST.get('subject_id')
    student_id = request.POST.get('student_id')

    assignment_mark = request.POST.get('assignment_mark', 0)
    attendance_mark = request.POST.get('attendance_mark', 0)
    exam_mark = request.POST.get('exam_mark', 0)

    if not student_id or not subject_id:
        messages.error(request, "Invalid student or subject selection.")
        return redirect('staff_add_result')

    try:
        get_student = Student.objects.get(id=int(student_id))
        get_subject = Subject.objects.get(id=int(subject_id))
    except (Student.DoesNotExist, Subject.DoesNotExist, ValueError):
        messages.error(request, "Selected student or subject does not exist.")
        return redirect('staff_add_result')

    result, created = Student_Result.objects.update_or_create(
        student_id=get_student,
        subject_id=get_subject,
        defaults={
            'assignment_mark': float(assignment_mark),
            'attendance_mark': float(attendance_mark),
            'exam_mark': float(exam_mark),
        }
    )

    if created:
        messages.success(request, "Result added successfully")
    else:
        messages.success(request, "Result updated successfully")

    return redirect('staff_add_result')

        

@login_required(login_url='/')
def staff_take_attendance(request):
    staff_id = Staff.objects.get(admin = request.user.id)
    subject = Subject.objects.filter(staff = staff_id)
    academic_years = Student.objects.values_list('academic_year', flat=True).distinct()
    action = request.GET.get('action')
    
    get_subject = None
    get_academic_year = None
    students = None
    
    if action is not None:
        if request.method == "POST":
            subject_id = request.POST.get('subject_id')
            get_academic_year = request.POST.get('academic_year')
            
            if subject_id and get_academic_year:
                get_subject = Subject.objects.get(id = subject_id)
                students = Student.objects.filter(course_id = get_subject.course_id, academic_year=get_academic_year)
    context = {
        'subject': subject,
        'action': action,
        'get_subject': get_subject,
        'get_academic_year': get_academic_year,
        'academic_years': academic_years,
        'students': students,
    }   
    return render(request, 'Staff/take_attendance.html', context)

@login_required(login_url='/')
def staff_save_attendance(request):
    if request.method != "POST":
        return redirect('staff_take_attendance')

    subject_id = request.POST.get('subject_id')
    attendance_date = request.POST.get('attendance_date')
    student_ids = request.POST.getlist('student_id')

    if not subject_id or not attendance_date:
        messages.error(request, "Subject and date are required")
        return redirect('staff_take_attendance')

    try:
        subject = Subject.objects.get(id=int(subject_id))
    except Subject.DoesNotExist:
        messages.error(request, "Subject not found")
        return redirect('staff_take_attendance')

    attendance, created = Attendance.objects.get_or_create(
        subject_id=subject,
        attendance_date=attendance_date
    )

    for stud_id in student_ids:
        try:
            student = Student.objects.get(id=int(stud_id))
        except Student.DoesNotExist:
            continue

        AtendanceReport.objects.get_or_create(
            student_id=student,
            attendance_id=attendance,
        )

    messages.success(request, "Attendance saved successfully")
    return redirect('staff_take_attendance')
 
        
@login_required(login_url='/')
def staff_view_attendance(request):
    staff_id = Staff.objects.get(admin=request.user.id)
    subjects = Subject.objects.filter(staff=staff_id)
    academic_years = Student.objects.values_list('academic_year', flat=True).distinct()
    
    action = request.GET.get('action')
    
    get_subject = None
    get_academic_year = None
    students = None
    attendance_records = None
    
    if action is not None:
        if request.method == "POST":
            subject_id = request.POST.get('subject_id')
            get_academic_year = request.POST.get('academic_year')
            
            if subject_id and get_academic_year:
                get_subject = Subject.objects.get(id=subject_id)
                
                # Get students of that course and academic year
                students = Student.objects.filter(
                    course_id=get_subject.course_id,
                    academic_year=get_academic_year
                )
                
                attendance_records = Attendance.objects.filter(
                    subject_id=get_subject.id,
                    student_id=students
                ).order_by('date')
    
    context = {
        'subjects': subjects,
        'action': action,
        'get_subject': get_subject,
        'get_academic_year': get_academic_year,
        'academic_years': academic_years,
        'students': students,
        'attendance_records': attendance_records,
    }
    
    return render(request, 'Staff/view_attendance.html', context)