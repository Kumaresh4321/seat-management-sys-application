from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import logout
from datetime import date, datetime,timedelta
from django.forms.models import model_to_dict

import random
import smtplib, ssl
from email.message import EmailMessage


def index(request):
    return render(request, 'pages/index.html')
def index2(request):
    return render(request, 'pages/index2.html')
def accordions(request):
    return render(request, 'pages/ui-features/accordions.html')
def badges(request):
    return render(request, 'pages/ui-features/badges.html')
def breadcrumbs(request):
    return render(request, 'pages/ui-features/breadcrumbs.html')
def buttons(request):
    return render(request, 'pages/ui-features/buttons.html')
def carousel(request):
    return render(request, 'pages/ui-features/carousel.html')
def clipboard(request):
    return render(request, 'pages/ui-features/clipboard.html')
def colcade(request):
    return render(request, 'pages/ui-features/colcade.html')
def contextmenu(request):
    return render(request, 'pages/ui-features/context-menu.html')
def dragula(request):
    return render(request, 'pages/ui-features/dragula.html')
def dropdowns(request):
    return render(request, 'pages/ui-features/dropdowns.html')
def loaders(request):
    return render(request, 'pages/ui-features/loaders.html')
def modals(request):
    return render(request, 'pages/ui-features/modals.html')
def notifications(request):
    return render(request, 'pages/ui-features/notifications.html')
def pagination(request):
    return render(request, 'pages/ui-features/pagination.html')
def popups(request):
    return render(request, 'pages/ui-features/popups.html')
def progress(request):
    return render(request, 'pages/ui-features/progress.html')
def slider(request):
    return render(request, 'pages/ui-features/slider.html')
def tabs(request):
    return render(request, 'pages/ui-features/tabs.html')
def tooltips(request):
    return render(request, 'pages/ui-features/tooltips.html')
def typography(request):
    return render(request, 'pages/ui-features/typography.html')
def basictable(request):
    return render(request, 'pages/tables/basic-table.html')
def datatable(request):
    return render(request, 'pages/tables/data-table.html')
def jsgrid(request):
    return render(request, 'pages/tables/js-grid.html')
def sortabletable(request):
    return render(request, 'pages/tables/sortable-table.html')
def widgets(request):
    return render(request, 'pages/widgets/widgets.html')
def calendar(request):
    return render(request, 'pages/apps/calendar.html')
def email(request):
    return render(request, 'pages/apps/email.html')
def gallery(request):
    return render(request, 'pages/apps/gallery.html')
def todo(request):
    return render(request, 'pages/apps/todo.html')
def c3(request):
    return render(request, 'pages/charts/c3.html')
def chartist(request):
    return render(request, 'pages/charts/chartist.html')
def chartjs(request):
    return render(request, 'pages/charts/chartjs.html')
def flotchart(request):
    return render(request, 'pages/charts/flot-chart.html')
def googlecharts(request):
    return render(request, 'pages/charts/google-charts.html')
def justGage(request):
    return render(request, 'pages/charts/justGage.html')
def morris(request):
    return render(request, 'pages/charts/morris.html')
def sparkline(request):
    return render(request, 'pages/charts/sparkline.html')
def advanced_elements(request):
    return render(request, 'pages/forms/advanced_elements.html')
def basic_elements(request):
    return render(request, 'pages/forms/basic_elements.html')
def code_editor(request):
    return render(request, 'pages/forms/code_editor.html')
def dropify(request):
    return render(request, 'pages/forms/dropify.html')
def text_editor(request):
    return render(request, 'pages/forms/text_editor.html')
def validation(request):
    return render(request, 'pages/forms/validation.html')
def wizard(request):
    return render(request, 'pages/forms/wizard.html')
def flagicons(request):
    return render(request, 'pages/icons/flag-icons.html')
def fontawesome(request):
    return render(request, 'pages/icons/font-awesome.html')
def mdi(request):
    return render(request, 'pages/icons/mdi.html')
def simplelineicon(request):
    return render(request, 'pages/icons/simple-line-icon.html')
def themify(request):
    return render(request, 'pages/icons/themify.html')
def googlemaps(request):
    return render(request, 'pages/maps/google-maps.html')
def mapael(request):
    return render(request, 'pages/maps/mapael.html')
def rtl(request):
    return render(request, 'pages/page-layouts/rtl.html')
def vectormap(request):
    return render(request, 'pages/maps/vector-map.html')
def blankpage(request):
    return render(request, 'pages/samples/blank-page.html')
def error404(request):
    return render(request, 'pages/samples/error-404.html')
def error500(request):
    return render(request, 'pages/samples/error-500.html')
def faq(request):
    return render(request, 'pages/samples/faq.html')
def faq2(request):
    return render(request, 'pages/samples/faq-2.html')
def invoice(request):
    return render(request, 'pages/samples/invoice.html')
def lockscreen(request):
    return render(request, 'pages/samples/lock-screen.html')
def login(request):
    return render(request, 'pages/samples/login.html')
def login2(request):
    return render(request, 'pages/samples/login-2.html')
def newsgrid(request):
    return render(request, 'pages/samples/news-grid.html')
def orders(request):
    return render(request, 'pages/samples/orders.html')
def portfolio(request):
    return render(request, 'pages/samples/portfolio.html')
def pricingtable(request):
    return render(request, 'pages/samples/pricing-table.html')
def profile(request):
    return render(request, 'pages/samples/profile.html')
def register(request):
    return render(request, 'pages/samples/register.html')
def register2(request):
    return render(request, 'pages/samples/register-2.html')
def searchresults(request):
    return render(request, 'pages/samples/search-results.html')
def timeline(request):
    return render(request, 'pages/samples/timeline.html')
