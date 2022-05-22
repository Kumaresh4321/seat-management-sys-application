from django.db import models

# Create your models here.
class rel_request(models.Model):
    request_id =models.CharField(max_length=50, unique=True)
    lh_name=models.CharField(max_length=50)
    lh_id=models.CharField(max_length=50)
    dh_name=models.CharField(max_length=50)
    dh_id=models.CharField(max_length=50)
    reason=models.CharField(blank=True,max_length=500)
    status=models.CharField(max_length=10, default="Pending")
