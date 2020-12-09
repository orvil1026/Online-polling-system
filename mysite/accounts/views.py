from django.http.response import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls.base import reverse_lazy
from .forms import UserRegistrationForm
from django.http import HttpResponse
from django.urls import reverse

# Create your views here.

def login_user(request):
      

    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
          
        if user is not None:
            
            login(request,user)        
            redirect_url = request.GET.get('next','home')
            return redirect(redirect_url)
            
                     
        else:
            messages.error(request,"Username or password is not correct",
                            extra_tags='alert alert-warning alert-dismissible fade show')

    return render(request,'accounts/login.html')                        


def logout_user(request):
    logout(request)
    return redirect('home')


def create_user(request):

    if request.method=='POST':
        check1=False
        check2=False
        check3=False

        form=UserRegistrationForm(request.POST)
        if form.is_valid():

            username=form.cleaned_data['username']
            password1=form.cleaned_data['password1']
            password2=form.cleaned_data['password2']
            email=form.cleaned_data['email']

            if password1!=password2:
                check1=True
                messages.error(request,'Password doesnt match!',
                                extra_tags='alert alert-warning alert-dismissible fade show ')

            if User.objects.filter(email=email).exists():
                check2=True
                messages.error(request,'Email already exists!',
                                extra_tags='alert alert-warning alert-dismissible fade show ')

            if User.objects.filter(username=username).exists():
                check3=True
                messages.error(request,'Username already exists!',
                                extra_tags='alert alert-warning alert-dismissible fade show ')
            
            if check1 or check2 or check3:

                messages.error(request,'Registration failed!',
                               extra_tags='alert alert-warning alert-dismissible fade show')

                return redirect('accounts:register')
            
            else:
                user=User.objects.create_user(username=username,password=password1,email=email)
                messages.success(request,'Thanks for registering!',
                                extra_tags='alert alert-success alert-dismissible fade show')
                return redirect('accounts:login')
    

    else:
        form=UserRegistrationForm()
    return render(request,'accounts/register.html',{'form':form})



    