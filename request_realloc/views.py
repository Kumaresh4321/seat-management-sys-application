from django.shortcuts import render
from .forms import requestForm
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage
from .models import rel_request
from employeedashboard.models import Employee
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import token_generator, token_generator2
from django.views import View

# Create your views here.
@login_required
def add_req(request):
    submitted = False
    if request.method == "POST":
        form = requestForm(request.POST)
        if form.is_valid():
            rob=form.save()
            print(rob)
            print("WOHOOOOOOOOOO")
            #UserObj = User.objects.get(username=q)
            q=form.cleaned_data['lh_id']
            q2 = form.cleaned_data['dh_id']
            User = get_user_model()
            UserObj =  User.objects.get(username=q)
            UserObj2 = User.objects.get(username=q2)
            EmpObj = Employee.objects.get(user=UserObj)

            em=UserObj.email
            em2 = UserObj2.email
            current_user = request.user
            ed = Employee.objects.get(employee_id=current_user.username)
            print(ed.employee_id)
            rob.employee_id = ed.employee_id
            rob.employee_name = ed.user.first_name + ' ' + ed.user.last_name
            rob.save()
            """
            em='shravyav20@gmail.com'
            em2=Employee.objects.get(user=current_user)
            em1=em2.department_head
            em=Employee.objects.get(user=em1)
            """
            uidb64 = urlsafe_base64_encode(force_bytes(rob.request_id))
            print(uidb64)
            domain=get_current_site(request).domain
            temp=token_generator.make_token(rob)
            temp2 = token_generator2.make_token(rob)
            print(temp)
            link=reverse('verify',kwargs={'uidb64':uidb64, 'token':temp })
            link2=reverse('verify2',kwargs={'uidb64':uidb64, 'token':temp2 })
            print(link)
            activate_url = 'http://'+domain+link
            activate_url2 = 'http://'+domain+link2
            email_bod = 'Hi line head '+UserObj.username+', Please use this link to give permission to '+current_user.username+ ' to change seats.\n' + activate_url
            email_bod2 = 'Hi department head'+UserObj2.username+', Please use this link to give permission to '+current_user.username+ ' to change seats.\n' + activate_url2



            email_sub='Please accept or deny seat change request for '+current_user.username
            email = EmailMessage(
                email_sub,
                email_bod,
                'noreply@semycolon.com',
                [em],
            )
            email2 = EmailMessage(
                email_sub,
                email_bod2,
                'noreply@semycolon.com',
                [em2],
            )
            email.send(fail_silently=False)
            email2.send(fail_silently=False)
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
        print("ANYA")
        # print(uidb64)
        # print(token)
        id = force_str(urlsafe_base64_decode(uidb64))
        #print(id)
        user = rel_request.objects.get(request_id=id)
        #print(user)
        #print(token_generator.check_token(user,token))
        if not token_generator.check_token(user,token):
        #         #return HttpResponseRedirect('login'+'?message='+'Request already accepted')
                print(user.lh_status)
                print("Already approved")
        #
        # if (user.status=="Approved"):
        #     print("Account already activated")

        if (user.lh_status=="Pending"):
            print("WAEEE")
            user.lh_status="Approved"
        #         #return HttpResponseRedirect('login')
        #     print("YO2")
        # user.is_active = True
        user.save()

        print('Account activated successfully')
        print(user.lh_status)
        #except Exception as ex:
            #pass
        return render(request, 'accept.html')

class VerificationView2(View):
    def get(self,request, uidb64, token):
        #print("TELL ME PLZ ")
        #try:
        print("ANYA")
        # print(uidb64)
        # print(token)
        id = force_str(urlsafe_base64_decode(uidb64))
        #print(id)
        user = rel_request.objects.get(request_id=id)
        #print(user)
        #print(token_generator.check_token(user,token))
        if not token_generator.check_token(user,token):
        #         #return HttpResponseRedirect('login'+'?message='+'Request already accepted')
                print(user.dhstatus)
                print("Already approved")
        #
        # if (user.status=="Approved"):
        #     print("Account already activated")

        if (user.dhstatus=="Pending"):
            print("WAEEE")
            user.dhstatus="Approved"
        #         #return HttpResponseRedirect('login')
        #     print("YO2")
        # user.is_active = True
        user.save()

        print('Account activated successfully')
        print(user.dhstatus)
        #except Exception as ex:
            #pass
        return render(request, 'accept.html')

# def empreq(request):
#     return render(request, 'accept.html', {})

# class VerificationView(View):
#     def get(self,request, uidb64, token):
#         return redirect('login')
