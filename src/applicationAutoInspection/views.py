#coding:utf-8
from .forms import ReportForm
from applicationAutoInspection.models import Report
from autoInspectionServer.settings import MEDIA_ROOT
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template.context import Context, RequestContext
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
from rexec import FileWrapper
import datetime
import os
import re
import time

#reporter_list = ['张三', '李四']
#report_list =  [Report(reporter_list[0],100, 100, '2015-05-29 18:00:00', 'D:\report\bj\2015\05\29\180000.pdf'),
#                Report(reporter_list[1],70, 70, '2015-05-29 18:30:00', 'D:\report\bj\2015\05\29\183000.pdf')]

# Create your views here.
def upload(request):
    t = get_template('upload.html')
    html = t.render(Context())
    return HttpResponse(html)

def handle_uploaded_file(f_report, f_log, system):
    '''
    f_report表示巡检人员提交的report.html文件
    f_log表示巡检人员提交的log.html文件
    system表示巡检的系统
    '''
    report_file_name = ""
    try:
        #在服务器上创建路径存储巡检人员提交的报告
        path = MEDIA_ROOT + system + time.strftime('/%Y/%m/%d/%H%M%S/')
        if not os.path.exists(path):
            os.makedirs(path)
        #将report.html和log.html存入服务器
        report_file_name = path + 'report.html'
        log_file_name = path + 'log.html'
        dest_report = open(report_file_name, 'wb+')
        all_report_text = f_report.read()
        dest_report.write(all_report_text)
        dest_report.close()
        dest_log = open(log_file_name, 'wb+')
        all_log_text = f_log.read()
        dest_log.write(all_log_text)
        dest_log.close()
        
        #抽取通过测试的数目和未通过的数目
        pattern = re.compile(r'"fail":\d+,"label":"All Tests","pass":\d+')
        match = pattern.search(all_report_text)
        str = match.group()
        nums = re.findall(r'\d+', str)
        fail_num = int(nums[0])
        pass_num = int(nums[1])
    except Exception, e:
        print e
    return report_file_name.replace(MEDIA_ROOT, 'report/'), fail_num + pass_num, pass_num


@csrf_exempt
def upload_report(request):
    
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            year, month, day, hour, minute, second, w, y, i = time.localtime( )
            report = Report(reporter = data['reporter'], system = data['system'], province = data['province'], city = data['city'], year = year, month = month, day = day, time = str(hour) + ':' + str(minute) + ':' + str(second))
            report.path, report.total_num, report.pass_num = handle_uploaded_file(request.FILES['report_file'], request.FILES['log_file'], report.system)
            report.save()    
            return HttpResponseRedirect('/success/')
    else:
        form = ReportForm()
    return render_to_response('upload.html', {'form': form})

def success(request):
    t = get_template('success.html')
    html = t.render(Context())
    return HttpResponse(html)   

def result(request):
    t = get_template('result.html')
    report_list = Report.objects.all()
    html = t.render(Context({'report_list' : report_list}))
    return HttpResponse(html)

#def download_report(request):
#    if request.method == 'POST':
#        filename = request['fileName']                    
#        wrapper = FileWrapper(file(filename))
#        response = HttpResponse(wrapper, content_type='text/plain')
#        response['Content-Length'] = os.path.getsize(filename)
#        response['Content-Encoding'] = 'utf-8'
#        response['Content-Disposition'] = 'attachment;filename=%s' % filename
#        return response
#    return render(request,'result.html',locals())    


    

