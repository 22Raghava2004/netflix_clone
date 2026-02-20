from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
def index(request):
    return render(request, "index.html")


def login(request):
    return render(request,'login.html')

def signup(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password2=request.POST['password2']

        if password==password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email already exists')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request,'username already exists')
                return redirect('signup')
            else:
                user=User.objects.create_user(username=username,email=email,password=password)
                user.save()
                
                #user login
                user_login=auth.authenticate(username=username,password=password)
                auth.login(request,user_login)
                return redirect('/')
        else:
            messages.info(request,'password not matching')
            return redirect('signup')
    else:
        return render(request,'signup.html')



@require_POST
def add_to_list(request):
    return JsonResponse({"message": "Added to List"})
