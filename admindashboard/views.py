from django.shortcuts import render
from employeedashboard.views import displayemployee
from django.contrib.auth.decorators import login_required
from employeedashboard.models import Employee
from seats.models import Seat

departments = ['Marketing', 'Operations', 'Finance', 'Sales', 'Human Resources', 'Technical']

# Create your views here.
@login_required(login_url='/accounts/login/')
def dashboard(request):
    #context = displayemployee(request, request.user)
    context = returnstats(request)
    return render(request, 'admin_dash.html', context)

@login_required(login_url='/accounts/login/')
def requests(request):
    #context = displayemployee(request, request.user)
    return render(request, 'allot_req.html', {})

@login_required
def returnstats(request):
    floor1_progress = []
    for dept in departments:
        floor1_progress.append(Seat.objects.filter(department_name=dept).filter(state='oc').count()*100/Seat.objects.filter(department_name=dept).count())
    context = {
    'reportname': 'Floorwise Report',
    'floor1_marketing': floor1_progress[0],
    'floor1_operations': floor1_progress[1],
    'floor1_finance': floor1_progress[2],
    'floor1_sales': floor1_progress[3],
    'floor1_hr': floor1_progress[4],
    'floor1_technical': floor1_progress[5],
    }
    return context
