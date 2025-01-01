from django.shortcuts import render, redirect, HttpResponse
from main.emailBackEnd import EmailBackend
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from main.models import CustomUser

def Base(request):
    return render(request, 'base.html')

def Login(request):
    return render(request, 'login.html')

def doLogin(request):
    if request.method == "POST":
        user = EmailBackend.authenticate(request, username=request.POST['email'], password=request.POST['password'])
        if user!=None:
            login(request, user)
            user_type = user.user_type
            if user_type =='1':
                return redirect('hod_home')
            elif user_type == '2':
                return redirect('staff_home')
            elif user_type == '3':
                return redirect('student_home')
            else:
                messages.error(request, 'Invalid Email or Password')
                return redirect('login')
        else:
            messages.error(request, 'Invalid Email or Password')
            return redirect('login')

def doLogout(request):
    logout(request)
    return redirect('login')

@login_required(login_url='/')
def profile(request):
    user = CustomUser.objects.get(id = request.user.id)
    context = {'user': user}
    return render(request, 'Profile/profile.html', context)

@login_required(login_url='/')
def edit_profile(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            customuser = CustomUser.objects.get(id = request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            if profile_pic != None and profile_pic != "":
                customuser.profile_pic = profile_pic
            customuser.save()
            messages.success(request, 'Your Profile has been updated!')
            return redirect('profile')
        except:
            messages.error(request, 'Your Profile could not be updated!')
            return redirect('profile')
    return render(request, 'edit_profile.html')