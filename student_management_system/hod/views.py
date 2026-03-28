from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from main.models import *
# ===================================Recommendation Algorithm==================================== #
def autocomplete_name(request):
    # Placeholder for recommendation algorithm logic
    query = request.GET.get('q', '')
    students = Student.objects.filter(Q(admin__first_name__icontains=query) | Q(admin__last_name__icontains=query))[0:10]
    results = [
        f"{st.admin.first_name} {st.admin.last_name}" for st in students
    ]
    return JsonResponse([
    {"id": st.id, "name": f"{st.first_name} {st.last_name}"}
    for st in students
], safe=False)


@login_required(login_url='/')
def home(request):
    student_count=Student.objects.all().count()
    student = Student.objects.all()
    staff_count=Staff.objects.all().count()
    staff = Staff.objects.all()
    course_count=Course.objects.all().count()
    subject_count=Subject.objects.all().count()
    context={
        'student_count':student_count,
        'student':student,
        'staff':staff,
        'subject_count':subject_count,
        'staff_count':staff_count,
        'course_count':course_count,
    }
    return render(request,'HOD/home.html', context)

# ===================================Student==================================== #

@login_required(login_url='/')
def add_student(request):
    course = Course.objects.all()
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        date_of_birth = request.POST.get('date_of_birth')
        academic_year = request.POST.get('academic_year')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        course_id = request.POST.get('course_id')

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, 'Email already registered.')
            return redirect('hod_add_student')
        
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, 'Username already registered.')
            return redirect('hod_add_student')
        else:
            user = CustomUser(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                profile_pic=profile_pic,
                user_type=3
            )
            user.set_password(password)
            user.save()

            course = Course.objects.get(id=course_id)

            student = Student(
                admin=user,
                address=address,
                date_of_birth = date_of_birth,
                academic_year = academic_year,
                course_id=course,
                gender=gender
            )
            student.save()
            messages.success(request, user.first_name + " " + user.last_name +' Added Successfully')
            return redirect('hod_view_student')

    context = {'course':course}
    return render(request,'HOD/Student/add_student.html', context)

@login_required(login_url='/')
def view_student(request):
    student = Student.objects.all()
    context = {'student':student}
    return render(request,'HOD/Student/view_student.html', context)

@login_required(login_url='/')
def edit_student(request,id):
    student = Student.objects.get(id=id)
    course = Course.objects.all()
    context = {'student':student,'course':course}
    return render(request,'HOD/Student/edit_student.html',context)

@login_required(login_url='/')
def update_student(request):
    if request.method == "POST":
        student_id = request.POST.get('student_id')
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        date_of_birth = request.POST.get('date_of_birth')
        academic_year = request.POST.get('academic_year')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        course_id = request.POST.get('course_id')

        user = CustomUser.objects.get(id=student_id)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username

        if password != None and password != "":
            user.set_password(password)
        if profile_pic != None and profile_pic != "":
            user.profile_pic = profile_pic
        user.save()

        student = Student.objects.get(admin=student_id)
        student.address=address
        student.date_of_birth=date_of_birth
        student.academic_year=academic_year
        student.gender=gender

        course  = Course.objects.get(id=course_id)
        student.course_id=course

        student.save()
        messages.success(request, user.first_name + " " + user.last_name +' Records are Updated Successfully')
        return redirect('hod_view_student')

    return render(request,'HOD/Student/edit_student.html')

@login_required(login_url='/')
def delete_student(request, admin):
    student = CustomUser.objects.get(id=admin)
    student.delete()
    messages.warning(request, student.first_name + " " + student.last_name +' Records are Deleted Successfully.')
    return redirect('hod_view_student')

# ===================================Course==================================== #

@login_required(login_url='/')
def add_course(request):
    if request.method == "POST":
        course_code = request.POST.get('course_code')
        course_name = request.POST.get('course_name')
        short_name =   request.POST.get('short_name')
        course = Course(
            name=course_name,
            course_code = course_code,
            short_name = short_name
            )
        course.save() 
        messages.success(request, 'Course Added Successfully.')
        return redirect('hod_view_course')
    return render(request, 'HOD/Course/add_course.html')

@login_required(login_url='/')
def view_course(request):
    course = Course.objects.all()
    context = {'course':course}
    return render(request,'HOD/Course/view_course.html',context)

@login_required(login_url='/')
def edit_course(request,id):
    course = Course.objects.get(id=id)
    context = {'course':course}
    return render(request,'HOD/Course/edit_course.html', context)

@login_required(login_url='/')
def update_course(request):
    if request.method == "POST":
        name = request.POST.get('course_name')
        course_code = request.POST.get('course_code')
        short_name = request.POST.get('short_name')
        course_id = request.POST.get('course_id')
        course = Course.objects.get(id=course_id)
        course.name = name
        course.course_code = course_code
        course.short_name = short_name
        course.save()
        messages.success(request, 'Course is Updated Successfully.')
        return redirect('hod_view_course')
    return render(request,'HOD/Course/edit_course.html')

@login_required(login_url='/')
def delete_course(request, id):
    course = Course.objects.get(id=id)
    course.delete()
    messages.success(request, 'Course is Deleted Successfully.')
    return redirect('hod_view_course')

# ===================================Staff==================================== #

@login_required(login_url='/')
def add_staff(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        date_of_birth = request.POST.get('date_of_birth')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, 'Email already registered.')
            return redirect('hod_add_staff')
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, 'Username already taken.')
            return redirect('hod_add_staff')
        else:
            user = CustomUser(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                profile_pic=profile_pic,
                user_type=2
            )
            user.set_password(password)
            user.save()

            staff = Staff(
                admin=user,
                address=address,
                date_of_birth=date_of_birth,
                gender=gender
            )
            staff.save()
            messages.success(request, 'Staff are successfully added.')
            return redirect('hod_view_staff')

    return render(request,'HOD/Staff/add_staff.html')

@login_required(login_url='/')
def view_staff(request):
    staff = Staff.objects.all()
    context = {'staff':staff}
    return render(request, 'HOD/Staff/view_staff.html',context)

@login_required(login_url='/')
def edit_staff(request,id):
    staff=Staff.objects.get(id=id)
    context = {'staff':staff}
    return render(request,'HOD/Staff/edit_staff.html',context)

@login_required(login_url='/')
def update_staff(request):
    if request.method == "POST":
        staff_id = request.POST.get('staff_id')
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        date_of_birth = request.POST.get('date_of_birth')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = CustomUser.objects.get(id=staff_id)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username

        if password != None and password != "":
            user.set_password(password)
        if profile_pic != None and profile_pic != "":
            user.profile_pic = profile_pic
        user.save()

        staff = Staff.objects.get(admin=staff_id)
        staff.gender = gender
        staff.address = address
        staff.date_of_birth = date_of_birth
        staff.save()
        messages.success(request, 'Staff is Updated Successfully.')
        return redirect('hod_view_staff')

    return render(request, 'HOD/Staff/edit_staff.html')

@login_required(login_url='/')
def delete_staff(request, admin):
    staff = CustomUser.objects.get(id=admin)
    staff.delete()
    messages.success(request, 'Staff is Deleted Successfully.')
    return redirect('hod_view_staff')

# ===================================Subject==================================== #

@login_required(login_url='/')
def add_subject(request):
    course = Course.objects.all()
    staff = Staff.objects.all()
    if request.method == 'POST':
        subject_code = request.POST.get('subject_code')
        subject_name = request.POST.get('subject_name')
        course_id = request.POST.get('course_id')
        staff_id = request.POST.get('staff_id')

        course = Course.objects.get(id=course_id)
        staff = Staff.objects.get(id=staff_id)

        subject = Subject(
            subject_code = subject_code,
            name=subject_name,
            course=course,
            staff=staff,
        )
        subject.save()
        messages.success(request, 'Subject is Added Successfully.')

        return redirect('hod_view_subject')
    context = {'staff':staff, 'course':course}
    return render(request, 'HOD/Subject/add_subject.html',context)

@login_required(login_url='/')
def view_subject(request):
    subject = Subject.objects.all()
    context = {'subject':subject}
    return render(request, 'HOD/Subject/view_subject.html',context)

@login_required(login_url='/')
def edit_subject(request, id):
    subject = Subject.objects.get(id=id)
    course = Course.objects.all()
    staff = Staff.objects.all()
    context = {'subject':subject, 'course':course,'staff':staff}
    return render(request, 'HOD/Subject/edit_subject.html',context)

@login_required(login_url='/') # type: ignore
def update_subject(request):
    if request.method == "POST":
        subject_id=request.POST.get('subject_id')
        subject_code = request.POST.get('subject_code')
        subject_name = request.POST.get('subject_name')
        course_id = request.POST.get('course_id')
        staff_id = request.POST.get('staff_id')
        course = Course.objects.get(id = course_id)
        staff = Staff.objects.get(id = staff_id)

        subject = Subject(
            id=subject_id,
            subject_code=subject_code,
            name=subject_name,
            course=course,
            staff=staff,
        )
        subject.save()
        messages.success(request, 'Subject is Updated Successfully.')
        return redirect('hod_view_subject')
    
@login_required(login_url='/')
def delete_subject(request, id):
    subject = Subject.objects.filter(id=id)
    subject.delete()
    messages.warning(request, 'Subject is Deleted Successfully.')
    return redirect('hod_view_subject')


@login_required(login_url='/')
def staff_send_notification(request):
    staff = Staff.objects.all()
    seen_notification = Staff_Notification.objects.all().order_by('-id')[0:5]
    context = {'staff':staff, 'seen_notification':seen_notification}
    return render(request, 'HOD/staff_send_notification.html',context)

@login_required(login_url='/') # type: ignore
def staff_save_notification(request):
    if request.method == "POST":
        staff_id = request.POST.get('staff_id')
        message = request.POST.get('message')
        staff = Staff.objects.get(admin=staff_id)
        staff_notification = Staff_Notification(
            staff_id=staff,
            message=message,
        )
        staff_notification.save()
        messages.success(request, 'Notification is send to staff Successfully.')
        return redirect('staff_send_notification')

@login_required(login_url='/')
def staff_leave_view(request):
    staff_leave= Staff_leave.objects.all()
    context = {'staff_leave':staff_leave}
    return render(request,'HOD/staff_leave.html',context)

@login_required(login_url='/')
def staff_approve_leave(request, id):
    leave = Staff_leave.objects.get(id=id)
    leave.status = 1
    leave.save()
    return redirect('staff_leave_view')

@login_required(login_url='/')
def staff_disapprove_leave(request, id):
    leave = Staff_leave.objects.get(id=id)
    leave.status = 2
    leave.save()
    return redirect('staff_leave_view')

@login_required(login_url='/')
def student_leave_view(request):
    student_leave= Student_leave.objects.all()
    context = {'student_leave':student_leave}
    return render(request,'HOD/student_leave.html',context)

@login_required(login_url='/')
def student_approve_leave(request, id):
    leave = Student_leave.objects.get(id=id)
    leave.status = 1
    leave.save()
    return redirect('student_leave_view')

@login_required(login_url='/')
def student_disapprove_leave(request, id):
    leave = Student_leave.objects.get(id=id)
    leave.status = 2
    leave.save()
    return redirect('student_leave_view')

@login_required(login_url='/')
def staff_feedback(request):
    feedback = Staff_feedback.objects.all()
    feedback_history = Staff_feedback.objects.all().order_by('-id')[0:5]
    context = {'feedback':feedback, 'feedback_history':feedback_history}
    return render(request, 'HOD/staff_feedback.html', context)

@login_required(login_url='/') # type: ignore
def staff_feedback_save(request):
    if request.method == "POST":
        feedback_id = request.POST.get('feedback_id')
        feedback_reply = request.POST.get('feedback_reply')

        feedback = Staff_feedback.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.status = 1
        feedback.save()
        return redirect('staff_feedback_reply')

@login_required(login_url='/')
def student_send_notification(request):
    student = Student.objects.all()
    seen_student_notification = Student_Notification.objects.all().order_by('-id')[0:5]
    context = {'student':student, 'seen_student_notification':seen_student_notification}
    return render(request, 'HOD/student_send_notification.html',context)

@login_required(login_url='/') # type: ignore
def student_save_notification(request):
    if request.method == "POST":
        student_id = request.POST.get('student_id')
        message = request.POST.get('message')
        student = Student.objects.get(admin=student_id)
        student_notification = Student_Notification(
            student_id=student,
            message=message,
        )
        student_notification.save()
        messages.success(request, 'Notification is send to student Successfully.')
        return redirect('student_send_notification')

@login_required(login_url='/')
def student_feedback(request):
    feedback = Student_feedback.objects.all()
    feedback_history = Student_feedback.objects.all().order_by('-id')[0:5]
    context = {'feedback': feedback, 'feedback_history':feedback_history}
    return render(request, 'HOD/student_feedback.html', context)

@login_required(login_url='/') # type: ignore
def student_feedback_save(request):
    if request.method == "POST":
        feedback_id = request.POST.get('feedback_id')
        feedback_reply = request.POST.get('feedback_reply')

        feedback = Student_feedback.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.status = 1
        feedback.save()
        return redirect('student_feedback_reply')

# ===================================Result==================================== #
@login_required(login_url='/')
def view_student_result(request):
    students = Student.objects.all()
    action = request.GET.get("action")

    if request.method == "POST":
        student_id = request.POST.get("student_id")

        if not student_id:
            messages.error(request, "Please select a student")
            return redirect("hod_view_result")

        result = Student_Result.objects.filter(
            student_id__admin__id=student_id
        )

        return render(request, "hod/view_result.html", {
            "action": "show",
            "result": result,
            "student_id": student_id
        })

    return render(request, "hod/view_result.html", {
        "students": students,
        "action": None
    })
    
    