from django.shortcuts import render, redirect
from employeedashboard.views import displayemployee
from django.contrib.auth.decorators import login_required
from employeedashboard.models import Employee
from seats.models import Seat
from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.pagesizes import A4
from datetime import datetime
import json
import math
from io import StringIO
import xlsxwriter
import csv
from .forms import allocateForm, bufferForm
from request_realloc.models import rel_request
from django.contrib import messages

# json_serializer = serializers.get_serializer("json")
departments = ['Marketing', 'Operations', 'Finance', 'Sales', 'Human Resources', 'Technical']

# Create your views here.
@login_required(login_url='/login/')
def dashboard(request):
    #context = displayemployee(request, request.user)
    context = returnstats(request)
    return render(request, 'admin_dash.html', context)

@login_required(login_url='/login/')
def requests(request):
    allrequests = rel_request.objects.all()
    if request.method == "POST":
        id_list = request.POST.getlist('boxes')
        print(id_list)
        for x in id_list:
            print(x)
            rel_request.objects.filter(pk=int(x)).update(approved=True)
        return redirect('dashboard')
    context = {'requests': allrequests}
    
    return render(request, 'allot_req.html', context)

@login_required(login_url='/login/')
def returnstats(request):
    floor1_progress = []
    floor1_progress_un = []
    floor1_progress_buf = []
    for dept in departments:
        floor1_progress.append(math.floor(Seat.objects.filter(department_name=dept).filter(state='oc').count()*100/(Seat.objects.filter(department_name=dept).count() + 1)))
        floor1_progress_un.append(math.floor(Seat.objects.filter(department_name=dept).filter(state='un').count()*100/(Seat.objects.filter(department_name=dept).count() + 1)))
        floor1_progress_buf.append(math.floor(Seat.objects.filter(department_name=dept).filter(state='bu').count()*100/(Seat.objects.filter(department_name=dept).count() + 1)))
    # print(floor1_progress_un)
    context = {
    'reportname_1': 'Floorwise Report: Occupied Seats',
    'floor1_marketing': floor1_progress[0],
    'floor1_operations': floor1_progress[1],
    'floor1_finance': floor1_progress[2],
    'floor1_sales': floor1_progress[3],
    'floor1_hr': floor1_progress[4],
    'floor1_technical': floor1_progress[5],
    'reportname_2': 'Floorwise Report: Unoccupied Seats',
    'floor1_marketing_un': floor1_progress_un[0],
    'floor1_operations_un': floor1_progress_un[1],
    'floor1_finance_un': floor1_progress_un[2],
    'floor1_sales_un': floor1_progress_un[3],
    'floor1_hr_un': floor1_progress_un[4],
    'floor1_technical_un': floor1_progress_un[5],
    'reportname_3': 'Floorwise Report: Buffer Seats',
    'floor1_marketing_buf': floor1_progress_buf[0],
    'floor1_operations_buf': floor1_progress_buf[1],
    'floor1_finance_buf': floor1_progress_buf[2],
    'floor1_sales_buf': floor1_progress_buf[3],
    'floor1_hr_buf': floor1_progress_buf[4],
    'floor1_technical_buf': floor1_progress_buf[5],
    }
    print(context)
    return context

@login_required(login_url='/login/')
def reports(request):
    return render(request, 'reports.html', {})

def gen_data(floors, depts, statuses):
    data = {}
    if floors:
        floor_info = {}
        for f in floors:
            occ = Seat.objects.filter(state='oc').filter(floor_number=f)

            unocc = Seat.objects.filter(state='un').filter(floor_number=f)
            buff = Seat.objects.filter(state='bu').filter(floor_number=f)
            floor_info[f] = {
            'Occupied': occ,
            'Unoccupied': unocc,
            'Buffer': buff
            }
        data['Floors'] = floor_info
    if depts:
        dept_info = {}
        for d in depts:
            occ = Seat.objects.filter(state='oc').filter(department_name=d)
            unocc = Seat.objects.filter(state='un').filter(department_name=d)
            buff = Seat.objects.filter(state='bu').filter(department_name=d)
            dept_info[d] = {
            'Occupied': occ,
            'Unoccupied': unocc,
            'Buffer': buff
            }
        data['Department'] = dept_info
    if statuses:
        status_info = {}
        for s in statuses:
            if s == "Occupied": st = "oc"
            if s == "Unoccupied": st = "un"
            if s == "Buffer": st = "bu"
            status_info[s] = {
            'Total' : Seat.objects.filter(state=st)
            }

        data['Status'] = status_info

    # print(data)

    return data


@login_required(login_url='/login/')
def generate_pdf(request):
    if request.method == 'POST':
        floors= request.POST.getlist('floor')
        depts = request.POST.getlist('dept')
        statuses = request.POST.getlist('status')
    # print(floors)

    data = {}
    if floors:
        floor_info = {}
        for f in floors:
            occ = Seat.objects.filter(state='oc').filter(floor_number=f)
            unocc = Seat.objects.filter(state='un').filter(floor_number=f)
            buff = Seat.objects.filter(state='bu').filter(floor_number=f)
            floor_info[f] = {
            'Occupied': occ,
            'Unoccupied': unocc,
            'Buffer': buff
            }
        data['Floors'] = floor_info
    if depts:
        dept_info = {}
        for d in depts:
            occ = Seat.objects.filter(state='oc').filter(department_name=d)
            unocc = Seat.objects.filter(state='un').filter(department_name=d)
            buff = Seat.objects.filter(state='bu').filter(department_name=d)
            dept_info[d] = {
            'Occupied': occ,
            'Unoccupied': unocc,
            'Buffer': buff
            }
        data['Department'] = dept_info
    if statuses:
        status_info = {}
        for s in statuses:
            if s == "Occupied": st = "oc"
            if s == "Unoccupied": st = "un"
            if s == "Buffer": st = "bu"
            status_info[s] = {
            'Total' : Seat.objects.filter(state=st)
            }

        data['Status'] = status_info

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Report.csv'

	# Create a csv writer
    writer = csv.writer(response)

    temp = 0
    if 'Floors' in data:

        temp1 = 0
        temp2 = 0
        if 'Status' in data:
            for k in statuses:
                temp1 = 0
                temp2 = 0
                if (k == 'Occupied'):
                    fields = ['Employee ID','First Name','Last Name','Designation','Location Name','Reporting to','Department Head','Shift ID','Tower','Floor Number','Seat Number']
                    writer.writerow(fields)
                    writer.writerow('')
                    for i in floors:
                        if 'Department' in data:
                            temp2 = 0
                            for j in depts:
                                for d in ((data['Floors'][floors[temp1]][k]) & (data['Department'][depts[temp2]][k])):
                                    ed = Employee.objects.filter(employee_id = d.employee_id)
                                    fields_temp = [ed[0].employee_id,ed[0].user.first_name,ed[0].user.last_name,ed[0].designation_name,ed[0].location_name,ed[0].reporting_to,ed[0].department_head,ed[0].shiftid,d.tower_id,d.floor_number,d.seat_number]
                                    writer.writerow(fields_temp)
                                temp2 += 1
                        temp1 += 1

                if (k == 'Buffer'):
                    writer.writerow('')
                    fields = ['Shift ID','Tower','Floor Number','Seat Number', 'Seat Status', 'Department']
                    writer.writerow(fields)
                    writer.writerow('')
                    for i in floors:
                        if 'Department' in data:
                            temp2 = 0
                            for j in depts:
                                for d in ((data['Floors'][floors[temp1]][k]) & (data['Department'][depts[temp2]][k])):
                                    fields_temp = [d.shiftid,d.tower_id,d.floor_number,d.seat_number,d.state,d.department_name]
                                    writer.writerow(fields_temp)
                                temp2 += 1
                        temp1 += 1

                if (temp == temp1):
                    if ((k == 'Unoccupied')):
                        writer.writerow('')
                        fields = ['Shift ID','Tower','Floor Number','Seat Number', 'Seat Status']
                        writer.writerow(fields)
                        writer.writerow('')
                        for i in floors:
                            if 'Department' in data:
                                temp2 = 0
                                for j in depts:
                                    for d in ((data['Floors'][floors[temp1]][k])):
                                        fields_temp = [d.shiftid,d.tower_id,d.floor_number,d.seat_number,'unoccupied']
                                        writer.writerow(fields_temp)
                                    temp2 += 1
                            temp1 += 1


    return response


@login_required()
def viewfloor1(request):
    context = {}
    info = request.POST.get('seat_number')
    context['seat_number'] = info
    if context is None:
        return render(request, 'floor.html', {})
    else:
        print(context)
        return render(request, 'floor.html', context)


def viewseatinfo(request):
    # context = json.loads()
    # print(context)
    context = {}
    info = request.POST.get('seat_number')[4:]
    context['seat_number'] = info
    st = Seat.objects.filter(seat_id = info)
    context['seat_id'] = st[0].seat_id
    context['seat_status'] = st[0].state
    context['seat_department_name'] = st[0].department_name
    context['seat_shiftid'] = st[0].shiftid
    context['employee_id'] = "null"
    if(st[0].employee_id != "null"):
        ed = Employee.objects.filter(employee_id = st[0].employee_id)
        context['employee_id'] = ed[0].employee_id
        context['employee_designation'] = ed[0].designation_name

    return render(request, 'seatinfo.html', context)

def allocateform(request, seat_id):
    context={}
    form = allocateForm(request.POST)
    context['seat_id'] = seat_id
    context['form'] = form
    print("hello")
    return render(request, 'allocationform.html', context)

def allocateseat(request, seat_id):
    print(seat_id)
    # if request.method == "POST":
    form = allocateForm(request.POST)
    if form.is_valid():
        empid = form.cleaned_data['employee_id']
        summa = Seat.objects.get(seat_id=seat_id)
        emp = Employee.objects.get(employee_id=empid)
        summa.employee_id = empid
        summa.state = 'oc'
        summa.department_name = emp.department_name
        summa.save()
    else:
        print(form.errors)
    return redirect('viewfloor1')

def bufferform(request, seat_id):
    context={}
    form = bufferForm(request.POST)
    context['seat_id'] = seat_id
    context['form'] = form
    print("hello")
    return render(request, 'bufferform.html', context)

def bufferseat(request, seat_id):
    print(seat_id)
    # if request.method == "POST":
    form = bufferForm(request.POST)
    if form.is_valid():
        print("vanakam")
        dept = form.cleaned_data['department_name']
        summa = Seat.objects.get(seat_id=seat_id)
        summa.state = 'bu'
        summa.department_name = dept
        summa.save()
    else:
        print(form.errors)
    return redirect('viewfloor1')

def deallocateseat(request, seat_id):
    if request.method == "GET":
        seat = Seat.objects.get(seat_id=seat_id)
        seat.department_name = 'null'
        seat.state = 'un'
        seat.employee_id = 'null'
        seat.save()
    return redirect('viewfloor1')

def loadsvg(request):
    return render(request, 'towera.svg', {})
