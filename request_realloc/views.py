from django.shortcuts import render, redirect
from .models import Request
from .forms import RequestForm
from django.http import HttpResponse

def submit_request(request):
    form = RequestForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('/employee/')
        else:
            return HttpResponse('Invalid Form')
    return render(request, "realloc_emp.html", {'form':form})
