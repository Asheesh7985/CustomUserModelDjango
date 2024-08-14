from django.shortcuts import render,HttpResponseRedirect
from .models import CustomUser
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.http import Http404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

# Create your views here.


def LoginPage(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                raise Http404("This email is not registerd!!!")
            
            CheckPassword = check_password(password, user.password)
            if CheckPassword:
                user= authenticate(email=email, password=password)
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect('/dashboard/')
                #messages.success(request, 'You Logged in successfully!!!')
                else:
                    messages.warning(request, 'Sorry, Please Check Your Email Or Password!!!')
            else:
                messages.warning(request, 'Password does not match!!!')
        return render(request, 'login.html')
    else:
        return HttpResponseRedirect('/dashboard/')

def SignupPage(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        father_name  = request.POST.get('fname')
        mother_name  = request.POST.get('mname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        village = request.POST.get('village')
        distric = request.POST.get('distric')
        pincode = request.POST.get('pincode')
        state = request.POST.get('state')
        password = request.POST.get('pwd')
        if CustomUser.objects.filter(email=email).filter():
            messages.warning(request, 'This Email Is Already Exists!!!')
        else:
            reg = CustomUser()
            reg.email = email
            reg.first_name = first_name
            reg.last_name = last_name
            reg.father_name = father_name
            reg.mother_name = mother_name
            reg.phone = phone
            reg.village = village
            reg.distric = distric
            reg.pincode = pincode
            reg.state = state
            reg.password = password
            reg.password = make_password(reg.password)
            reg.save()
            """
            reg = CustomUser(first_name=first_name, last_name=last_name,father_name=father_name,mother_name=mother_name,email=email, 
                            phone=phone,village=village,distric=distric,pincode=pincode,state=state,
                            password=password)
            reg.save()
            """
            #messages.success(request, 'Account Created Successfully!!!')
            return render(request, 'user.html',{'user':reg})

    return render(request, 'signup.html')

@login_required(login_url='login')
def DashboardPage(request):
    return render(request, 'dashboard.html')

@login_required(login_url='login')
def LogoutPage(request):
    logout(request)
    return HttpResponseRedirect('/login/')


def ForgetPasswordView(request):
    return render(request, 'forgetpassword.html')
