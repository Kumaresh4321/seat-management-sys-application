from django.shortcuts import render
from .forms import requestForm
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage
from .models import rel_request
from employeedashboard.models import Employee
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import token_generator
from django.views import View

# Create your views here.
@login_required
def add_req(request):
    submitted = False
    if request.method == "POST":
        form = requestForm(request.POST)
        if form.is_valid():
            form.save()
            #UserObj = User.objects.get(username=q)
            q=form.cleaned_data['lh_id']
            User = get_user_model()
            UserObj =  User.objects.get(username=q)
            EmpObj = Employee.objects.get(user=UserObj)

            em=UserObj.email
            current_user = request.user
            """
            em='shravyav20@gmail.com'
            em2=Employee.objects.get(user=current_user)
            em1=em2.department_head
            em=Employee.objects.get(user=em1)
            """
            uidb64 = urlsafe_base64_encode(force_bytes(current_user.pk))
            print(uidb64)
            domain=get_current_site(request).domain
            temp=token_generator.make_token(UserObj)
            print(temp)
            link=reverse('verify',kwargs={'uidb64':uidb64, 'token':temp })
            print(link)
            activate_url = 'http://'+domain+link
            email_bod = 'Hi '+UserObj.username+', Please use this link to give permission to '+current_user.username+ ' to change seats.\n' + activate_url


            email_sub='Please accept or deny seat change request for '+current_user.username
            email = EmailMessage(
                email_sub,
                email_bod,
                'noreply@semycolon.com',
                [em],
            )
            email.send(fail_silently=False)
            return HttpResponseRedirect('/seatrequests?submitted=True')

    else:
        form = requestForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'realloc_emp.html',{'form':form, 'submitted':submitted})

class VerificationView(View):
    def get(self,request, uidb64, token):
        #print("TELL ME PLZ ")
        #try:
        #print("ANYA ")
        # print(uidb64)
        # print(token)
        id = force_text(urlsafe_base64_decode(uidb64))
        #print(id)
        user = User.objects.get(pk=id)
            #print("OR2")
            #print("Heh "+user)
            #print("OR")

        if not token_generator.check_token(user,token):
                #return HttpResponseRedirect('login'+'?message='+'Request already accepted')
                print(user.is_active)

        if user.is_active:
                #return HttpResponseRedirect('login')
            print("YO2")
        user.is_active = True
        user.save()

        print('Account activated successfully')
        #except Exception as ex:
            #pass
        return render(request, 'accept.html')

# def empreq(request):
#     return render(request, 'accept.html', {})

# class VerificationView(View):
#     def get(self,request, uidb64, token):
#         return redirect('login')
