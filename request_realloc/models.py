from django.db import models

# Create your models here.
class rel_request(models.Model):
    request_id =models.AutoField(primary_key=True)
    employee_id = models.CharField(max_length=50)
    employee_name = models.CharField(max_length=50)
    lh_name=models.CharField(max_length=50)
    lh_id=models.CharField(max_length=50)
    dh_name=models.CharField(max_length=50)
    dh_id=models.CharField(max_length=50)
    reason=models.CharField(blank=True,max_length=500)
    lh_status=models.CharField(max_length=10, default="Pending")
    dhstatus=models.CharField(max_length=10, default="Pending")
    approved = models.BooleanField(default=False)
