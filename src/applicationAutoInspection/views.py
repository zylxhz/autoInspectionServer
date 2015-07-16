#coding:utf-8
from .forms import ReportForm
from applicationAutoInspection.models import Report, System
from autoInspectionServer.settings import MEDIA_ROOT
from django.core.files.storage import default_storage
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import F
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import Context
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
import datetime
import os
import re
import time
import zipfile


# Create your views here.

#每页展示的报告数目
REPORT_PER_PAGE = 50;
    
def upload(request):
    t = get_template('upload.html')
    html = t.render(Context())
    return HttpResponse(html)

def handle_uploaded_file(f, system, province, reporter):
    '''
    zip表示提交的报告压缩文件
    system表示巡检的系统
    province表示所在的省
    '''
    report_path = ""
        #在服务器上创建路径存储巡检人员提交的报告
    try:
        path = MEDIA_ROOT + system + os.path.sep + province + os.path.sep + reporter + time.strftime('\\%Y\\%m\\%d\\%H%M%S\\')
        if not os.path.exists(path):
            os.makedirs(path)
        zip_file = open('report.zip', 'wb+')
        for chunk in f.chunks():
            zip_file.write(chunk)
        zip_file.close()
        zip = zipfile.ZipFile('report.zip')
        for filename in zip.namelist():
            data = zip.read(filename)
            filename = os.path.split(filename)[1]
            file = open(os.path.join(path, filename), 'wb+')
            file.write(data)
            file.close()
            if filename == 'report.html':
                report_path = os.path.join(path, filename)
                report_path = report_path.replace(MEDIA_ROOT, '')
                #抽取通过测试的数目和未通过的数目
                pattern = re.compile(r'"fail":\d+,"label":"All Tests","pass":\d+')
                match = pattern.search(data)
                str = match.group()
                nums = re.findall(r'\d+', str)
                fail_num = int(nums[0])
                pass_num = int(nums[1])
    except Exception, e:
        print e
    return report_path, fail_num + pass_num, pass_num


@csrf_exempt
def upload_report(request):
      
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
#            instance = Report(reporter = data['reporter'], system = data['system'], province = data['province'], city = data['city'], report_file=request.FILES['report_file'], log_file=request.FILES['log_file'])
#            all_report_text = request.FILES['report_file'].read()
#            #抽取通过测试的数目和未通过的数目
#            pattern = re.compile(r'"fail":\d+,"label":"All Tests","pass":\d+')
#            match = pattern.search(all_report_text)
#            match_str = match.group()
#            nums = re.findall(r'\d+', match_str)
#            fail_num = int(nums[0])
#            pass_num = int(nums[1])
#            instance.pass_num = pass_num
#            instance.total_num = fail_num + pass_num             
#            instance.save()
            report_path, total_num, pass_num = handle_uploaded_file(request.FILES['zip'], data['system'], data['province'], data['reporter'])
            report_url = default_storage.url(report_path)
            instance = Report(reporter = data['reporter'], system = data['system'], province = data['province'], city = data['city'], total_num = total_num, pass_num = pass_num, report_path = report_url)
            instance.save()
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
    systems = System.objects.all()
    context = {'systems': systems}
    html = t.render(context)
    return HttpResponse(html) 

def search(request):
    q_system = request.REQUEST['system']
    q_reporter = request.REQUEST['reporter']
    q_province = request.REQUEST['province']
    q_city = request.REQUEST['city']
    q_begin_date = request.REQUEST['begin_date']
    q_end_date = request.REQUEST['end_date']
    end_date = datetime.datetime.strptime(q_end_date,'%Y-%m-%d')
    end_date = end_date +  datetime.timedelta(days=1)
    q_end_date = end_date.strftime('%Y-%m-%d')
    q_status = request.REQUEST['status'] 
    report_list = Report.objects.all()
    if q_system != '':
        report_list = report_list.filter(system=q_system)
    if q_reporter != '':
        report_list = report_list.filter(reporter=q_reporter)
    if q_province != '':
        report_list = report_list.filter(province=q_province)
    if q_city != '':
        report_list = report_list.filter(city=q_city)
    if q_begin_date != '':
        report_list = report_list.filter(sub_time__gte=q_begin_date)
    if q_end_date != '':
        report_list = report_list.filter(sub_time__lt=q_end_date)
    if q_status == 'fail':
        report_list = report_list.exclude(total_num=F('pass_num'))
    if q_status == 'pass':
        report_list = report_list.filter(total_num=F('pass_num'))
    #对查询结果进行排序，先按系统名称的升序排序，然后按照提交日期降序排序。
    report_list = report_list.order_by('system', '-sub_time')
    #分页
    paginator = Paginator(report_list, REPORT_PER_PAGE)
    page = request.GET.get('page')
    try:
        reports = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        reports = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        reports = paginator.page(paginator.num_pages)

    return render_to_response('report_list_div.html', {"reports": reports})


    

