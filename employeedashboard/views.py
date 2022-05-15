from django.shortcuts import render
from django.contrib.auth import logout
from .models import Employee
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def emphome(request):
    context = displayemployee(request, request.user)
    return render(request, 'employee_dash.html', context)

@login_required
def empreq(request):
    context = displayemployee(request, request.user)
    return render(request, 'realloc_emp.html', context)

@login_required
def displayemployee(request, user):
    emp_user = user.username
    print(emp_user)
    emp = Employee.objects.filter(email_id=emp_user)
    print(emp[0].first_name)
    context = {
    'employee_name' : emp[0].first_name,
    'emp_id' : emp[0].employee_id,
    }
    return context
