from django.shortcuts import render

# Create your views here.
def emphome(request):
    return render(request, 'employee_dash.html', {})

def empreq(request):
    return render(request, 'realloc_emp.html', {})
