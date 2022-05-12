from django.db import models

# Create your models here.
class Employee(models.Model):
    employee_id = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email_id = models.EmailField(max_length=254, unique=True)
    designation = models.CharField(max_length=50)
    reporting_to = models.CharField(max_length=50)
    department_head = models.CharField(max_length=80)
    department = models.CharField(max_length=80)
    shift = models.CharField(max_length=50)
