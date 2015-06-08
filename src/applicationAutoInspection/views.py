#coding:utf-8
from .forms import ReportForm
from applicationAutoInspection.report import Report
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template.context import Context
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
import datetime
import os
import time

project_team_list = ['北京项目组', 
                     '上海项目组']
report_list =  [Report(project_team_list[0],100, 100, '2015-05-29 18:00:00', 'D:\report\bj\2015\05\29\180000.pdf'),
                Report(project_team_list[1],70, 70, '2015-05-29 18:30:00', 'D:\report\bj\2015\05\29\183000.pdf')]

# Create your views here.
def upload(request):
    t = get_template('upload.html')
    html = t.render(Context())
    return HttpResponse(html)

def handle_uploaded_file(f, project_team_id):
    file_name = ""
    try:
        path = "D:/report/" + project_team_id + time.strftime('/%Y/%m/%d/')
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
            pro_id = int(data['projectTeamID'])
            report_list[pro_id].time = time.strftime('%Y-%m-%d %H:%M:%S')
            report_list[pro_id].link = handle_uploaded_file(request.FILES['file'], pro_id)
            report_list[pro_id].test_num = data['testNum']
            report_list[pro_id].pass_num = data['passNum']        
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
    html = t.render(Context({'report_list' : report_list}))
    return HttpResponse(html)  

