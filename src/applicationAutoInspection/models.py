from django.db import models

# Create your models here.
class Report(models.Model):
    reporter = models.CharField(max_length=100)
    system = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    sub_time = models.DateTimeField('Time submitted',auto_now=True)
    total_num = models.IntegerField()
    pass_num = models.IntegerField()
    path = models.CharField(max_length=200)