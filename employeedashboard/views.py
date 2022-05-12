from django.shortcuts import render
from .models import Employee

# Create your views here.
def emphome(request):
    return render(request, 'employee_dash.html', {})

def empreq(request):
    return render(request, 'realloc_emp.html', {})

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
