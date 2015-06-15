#coding:utf-8
from .forms import ReportForm
from applicationAutoInspection.models import Report
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template.context import Context, RequestContext
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
from rexec import FileWrapper
import datetime
import os
import time

#reporter_list = ['张三', '李四']
#report_list =  [Report(reporter_list[0],100, 100, '2015-05-29 18:00:00', 'D:\report\bj\2015\05\29\180000.pdf'),
#                Report(reporter_list[1],70, 70, '2015-05-29 18:30:00', 'D:\report\bj\2015\05\29\183000.pdf')]

# Create your views here.
def upload(request):
    t = get_template('upload.html')
    html = t.render(Context())
    return HttpResponse(html)

def handle_uploaded_file(f, project):
    file_name = ""
    try:
        path = "D:/report/" + project + time.strftime('/%Y/%m/%d/')
        if not os.path.exists(path):
            os.makedirs(path)
            suffix = os.path.splitext(f.name)[1]
            file_name = path + time.strftime('%H%M%S') + suffix
            destination = open(file_name, 'wb+')
            for chunk in f.chunks():
                destination.write(chunk)
            destination.close()
    except Exception, e:
        print e
    return file_name

@csrf_exempt
def upload_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            year, month, day, hour, minute, second = time.localtime( )
            report = Report(reportor = data['reportor'], system = data['system'], province = data['province'], city = data['city'], year = year, month = month, day = day, time = hour + ':' + minute + ':' + second, total_num = data['testNum'], pass_num = data['passNum'])
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

def download_report(request):
    if request.method == 'POST':
        filename = request['fileName']                    
        wrapper = FileWrapper(file(filename))
        response = HttpResponse(wrapper, content_type='text/plain')
        response['Content-Length'] = os.path.getsize(filename)
        response['Content-Encoding'] = 'utf-8'
        response['Content-Disposition'] = 'attachment;filename=%s' % filename
        return response
    return render(request,'result.html',locals())    


    

