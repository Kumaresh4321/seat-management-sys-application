from django.db import models

class Request(models.Model):
    line_head_name = models.CharField(max_length=50)
    line_head_id = models.CharField(max_length=50)
    dept_head_name = models.CharField(max_length=50)
    dept_head_id = models.CharField(max_length=50)
    req_reason = models.TextField()
