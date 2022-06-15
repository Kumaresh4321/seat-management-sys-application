from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from seats.models import Seat
# Create your models here.
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    employee_id = models.CharField(max_length=50)
    designation_name = models.CharField(max_length=50)
    location_name = models.CharField(max_length=50)
    reporting_to = models.CharField(max_length=50)
    department_head = models.CharField(max_length=80)
    shiftid = models.CharField(max_length=6, choices=(
        ('ap', 'APAC'),
        ('uk',  'UK'),
    ), default='UK')
    department_name = models.CharField(max_length=50, null=True)
    seat_id = models.IntegerField(default = 0)
    reallocation_status = models.CharField(max_length=10, choices=(
        ('active', 'ACTIVE'),
        ('inactive', 'INACTIVE'),
    ), default='INACTIVE')


@receiver(post_save, sender=User) #whenever there is a create event for user, create a employee object
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Employee.objects.create(user=instance)

@receiver(post_save, sender=User) #after a save event, update model
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
