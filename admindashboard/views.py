from django.shortcuts import render
from employeedashboard.views import displayemployee
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def dashboard(request):
    context = displayemployee(request, request.user)
    return render(request, 'admin_dash.html', context)
    
@login_required
def requests(request):
    context = displayemployee(request, request.user)
    return render(request, 'allot_req.html', context)
