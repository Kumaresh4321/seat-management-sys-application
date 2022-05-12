from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from employeedashboard.views import displayemployee
from employeedashboard.models import Employee

# Create your views here.
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                context = displayemployee(request, user)
                return render(request, 'employee_dash.html', context)
            if user.is_superuser:
                context = displayemployee(request, user)
                return render(request, 'admin_dash.html', context)
        else:
            messages.success(request, ("There was an error, Try again"))
            return HttpResponseRedirect(reverse('Login_user'))
    else:
        return render(request, 'registration/login.html', {})
