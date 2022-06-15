from employeedashboard.models import Employee
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
#from django.conf import settings
from django.contrib.auth.hashers import make_password

import csv


def run():
    User = get_user_model()
    data = csv.reader(open('scripts/employee.csv'), delimiter=",")
    # User.objects.all().delete()
    # Employee.objects.all().delete()
    for row in data:
        Post = User()
        # Post.id = int(row[0])
        Post.username = row[1]
        Post.password = make_password(row[2])
        Post.first_name = row [4]
        Post.last_name = row[5]
        Post.email_address = row[6]
        Post.is_active ="1"
        if row[6].find("Admin") != -1:
            Post.is_staff = "1"
        Post.save()
        Post1, created = Employee.objects.get_or_create(user=Post)
        if not created:
            Post1.employee_id = row[3]
            Post1.designation_name = row[7]
            Post1.location_name = row[8]
            Post1.reporting_to = row[9]
            Post1.department_head = row[10]
            Post1.shiftid = row[11]
            Post1.department_name = row[12]
            Post1.seat_id = row[13]
            Post1.reallocation_status = row[14]
            Post1.save()
