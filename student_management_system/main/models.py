import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from datetime import timedelta

def date_of_birth_validate(Student):
    if Student.date_of_birth < datetime.date.today():
        raise ValidationError("Date Must Be future.")

def academic_year_validate(Student):
    current_year = datetime.date.today().year
    if Student.academic_year < str(current_year) or Student.academic_year > str(current_year + 1):
        raise ValidationError("Academic year must be current year or next year.")

def attendance_validate(Attendance):
    if Attendance.attendance_date != datetime.date.today():
        raise ValidationError("Attendance can only be taken for today.")
    
# Create your models here.
class CustomUser(AbstractUser):
    USERTYPE = (
        ('1','HOD'),
        ('2','Staff'),
        ('3','Student'),
    )
    user_type = models.CharField(choices= USERTYPE, max_length= 50, default= '1')
    profile_pic = models.ImageField(upload_to='media/profile_pic')

class Course(models.Model):
    name = models.CharField(max_length= 100)
    short_name = models.CharField(max_length=50, null=True)
    course_code = models.CharField(max_length=100, unique=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

class Student(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.CharField(max_length= 100)
    gender = models.CharField(max_length= 100)
    date_of_birth = models.DateField(null=True, validators=[date_of_birth_validate])
    course_id = models.ForeignKey(Course, on_delete=models.DO_NOTHING)
    academic_year = models.TextField(validators=[academic_year_validate])
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.admin.first_name + " " + self.admin.last_name

class Staff(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.CharField(max_length= 100)
    gender = models.CharField(max_length= 100)
    date_of_birth = models.DateField(null=True, validators=[date_of_birth_validate])
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.admin.username

class Subject(models.Model):
    objects = None
    name = models.CharField(max_length= 100)
    subject_code = models.CharField(max_length= 100, unique=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Staff_Notification(models.Model):
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    message = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(null=True,default=0)
    def __str__(self):
        return self.staff_id.admin.first_name  + " " + self.staff_id.admin.last_name

class Staff_leave(models.Model):
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    leave_date = models.DateTimeField(null=True)
    message = models.TextField()
    status = models.IntegerField(null=True,default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.staff_id.admin.first_name +" " + self.staff_id.admin.last_name

class Student_leave(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    leave_date = models.DateTimeField(null=True)
    message = models.TextField()
    status = models.IntegerField(null=True,default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.student_id.admin.first_name +" " + self.student_id.admin.last_name
    
class Student_Notification(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    message = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(null=True,default=0)
    
    def __str__(self):
        return self.student_id.admin.first_name  + " " + self.student_id.admin.last_name

class Staff_feedback(models.Model):
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    status = models.IntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.staff_id.admin.first_name +" " + self.staff_id.admin.last_name

class Student_feedback(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    status = models.IntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.student_id.admin.first_name +" " + self.student_id.admin.last_name

class Student_Result(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE)
    assignment_mark = models.FloatField(default=0)
    attendance_mark = models.FloatField(default=0)
    exam_mark = models.FloatField(default=0)
    final_result = models.FloatField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.student_id.admin.first_name +" " + self.student_id.admin.last_name
    
class Attendance(models.Model):
    subject_id = models.ForeignKey(Subject, on_delete=models.DO_NOTHING)
    attendance_date = models.DateField(validators=[attendance_validate])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
        
    def __str__(self):
        return self.subject_id.name
        
class AtendanceReport(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    attendance_id = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
        
    def __str__(self):
        return self.student_id.admin.first_name
            
        
        
        