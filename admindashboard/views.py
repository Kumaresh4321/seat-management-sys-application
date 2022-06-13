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
    #context = displayemployee(request, request.user)
    return render(request, 'allot_req.html', {})

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
                                        fields_temp = [d.shiftid,d.tower_id,d.floor_number,d.seat_number,d.state]
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
    context['seat_status'] = st[0].state
    context['seat_department_name'] = st[0].department_name
    context['seat_shiftid'] = st[0].shiftid
    context['employee_id'] = "null"
    if(st[0].employee_id != "null"):
        ed = Employee.objects.filter(employee_id = st[0].employee_id)
        context['employee_id'] = ed[0].employee_id
        context['employee_designation'] = ed[0].designation_name

    return render(request, 'seatinfo.html', context)

def allocateform(request):
    return render(request, 'allocationform.html', {})

def allocateseat(request):
    if request.method == "POST":
        form = requestForm(request.POST)
        if form.is_valid():
            print("form", form)
    return render(request, 'reports.html', {})

def loadsvg(request):
    return render(request, 'towera.svg', {})
