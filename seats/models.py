from django.db import models
from django.db.models import Value


class Seat(models.Model):
    seat_number = models.IntegerField()
    floor_number = models.CharField(max_length=6, choices=(('1','One'),
    ('2', 'Two')))
    tower_id = models.CharField(max_length=6, choices=(('A', 'Tower A'),('B', 'Tower B')))
    state = models.CharField(max_length=6, choices=(
        ('oc','Occupied'),
        ('un', 'Unoccupied'),
        ('bu', 'Buffer'),
        ), default='Unoccupied')
    shiftid = models.CharField(max_length=6, choices=(
        ('ap', 'APAC'),
        ('uk',  'UK'),
    ), default='UK')
    department_name = models.CharField(max_length=50, null=True)
    auto_increment_id = models.AutoField(primary_key=True)
