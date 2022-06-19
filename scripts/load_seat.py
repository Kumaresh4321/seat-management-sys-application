from employeedashboard.models import Employee
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
#from django.conf import settings
from django.contrib.auth.hashers import make_password
from seats.models import Seat
import csv


def run():
    # User = get_user_model()
    data = csv.reader(open('scripts/bothFloors.csv'), delimiter=",")
    # User.objects.all().delete()
    # Employee.objects.all().delete()
    for row in data:
        Post = Seat()
        Post.id = row[0]
        Post.seat_number = row[1]
        Post.floor_number = row[2]
        Post.tower_id = row[3]
        Post.state = row[4]
        Post.shiftid = row[5]
        Post.department_name = row[6]
        Post.seat_id = row[7]
        Post.employee_id = row[8]
        Post.save()
