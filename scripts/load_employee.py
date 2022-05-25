from employeedashboard.models import Employee
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
#from django.conf import settings
from django.contrib.auth.hashers import make_password

import csv


def run():
    User = get_user_model()
    data = csv.reader(open('scripts/EmployeeTemplate.csv'), delimiter=",")
    User.objects.all().delete()
    Employee.objects.all().delete()
    for row in data:
        Post = User()
        #Post.id = row[0]
        Post.username = row[1]
        Post.password = make_password(row[2])
        Post.first_name = row [3]
        Post.last_name = row[4]
        Post.email_address = row[5]
        Post.is_active ="1"
        if row[6].find("Admin") != -1:
            Post.is_staff = "1"
        Post.save()
        Post1, created = Employee.objects.get_or_create(user=Post)
        if not created:
            Post1.designation_name = row[6]
            Post1.location_name = row[7]
            Post1.reporting_to = row[8]
            Post1.department_head = row[9]
            Post1.shift = row[10]
            Post1.save()
