from django.shortcuts import render,redirect
from django.contrib.auth import logout
from .models import Employee
from seats.models import Seat
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def emphome(request):
    emp_user = request.user
    emp = Employee.objects.get(user=emp_user)
    print(emp)
    seat = Seat.objects.get(seat_id=emp.seat_id)
    print(seat)
    context={
        'cuser' : emp_user,
        'seat' : seat,
    }
    # context['u_floor'] = info
    # st = Seat.objects.filter(seat_id = info)
    # context['seat_id'] = st[0].seat_id
    # context['seat_status'] = st[0].state
    return render(request, 'employee_dash.html', context)

@login_required
def empreq(request):
    return render(request, 'realloc_emp.html', {})

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
