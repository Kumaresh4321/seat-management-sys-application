from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from employeedashboard.views import displayemployee
from employeedashboard.models import Employee
from django.views.csrf import csrf_failure
from django.views.decorators.cache import cache_control
from admindashboard.views import dashboard
# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect ('/dashboard/')
            else:
                return render(request, 'employee_dash.html', {})
        else:
            messages.success(request, ("There was an error, Try again"))
            return HttpResponseRedirect('/accounts/login/')
    else:
        return render(request, 'registration/login.html', {})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout_user(request):
    logout(request)
    csrf_failure(request)
    return redirect('/login/')

def csrf_failure(request, reason=""):
    #ctx = {'message': 'some custom messages'}
    return redirect('/login/')
