from django.shortcuts import render
from employeedashboard.views import displayemployee
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='/accounts/login/')
def dashboard(request):
    #context = displayemployee(request, request.user)
    return render(request, 'admin_dash.html', {})

@login_required(login_url='/accounts/login/')
def requests(request):
    #context = displayemployee(request, request.user)
    return render(request, 'allot_req.html', {})
