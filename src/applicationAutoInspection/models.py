#coding:utf-8
from django.db import models

# Create your models here.
class Report(models.Model):
    reporter = models.CharField(u'报告提交人', max_length=100)
    system = models.CharField(u'系统',  max_length=100)
    province = models.CharField(u'省份', max_length=100)
    city = models.CharField(u'城市', max_length=100)
    sub_time = models.DateTimeField(u'提交日期',auto_now=True)
    total_num = models.IntegerField(u'测试用例数目')
    pass_num = models.IntegerField(u'通过测试的数目')
    report_file = models.FileField(u'报告', upload_to='report/%Y/%m/%d/%H%M%S')
    log_file = models.FileField(upload_to='report/%Y/%m/%d/%H%M%S')
    
class System(models.Model):
    name = models.CharField(u'系统',  max_length=100)