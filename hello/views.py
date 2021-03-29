from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import Study, Profile, User
from .forms import StudyForm, FindForm, FindYearForm, ProfileForm, SignUpForm
from django.db.models import Q
from django.db.models import Count, Sum, Max
import datetime
from datetime import date
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
mpl.use('Agg')
plt.rcParams['font.family'] = 'AppleGothic'
mpl.rcParams['font.family'] = 'AppleGothic'
import io

now = timezone.localtime(timezone.now())
#now = datetime.datetime.now()
now_year = now.year
now_month = now.month
now_day = now.day
today_list = [now_year, now_month, now_day]

@login_required
def index(request):
    global x, y, y_month, z_target
    x = []
    y = []
    y_month = []
    z_target = []
    x.clear()
    y.clear()
    y_month.clear()
    z_target.clear()
    judge = 0
    y_total = 0
    target_total = 0
    total = 0
    study_day = 0
    rate = '0.0 %'
    profile = None
    data = Study.objects.filter(owner=request.user)
    data = data.filter(year=now_year, month=now_month).order_by('day').reverse()
    isprof = Profile.objects.filter(owner=request.user).count()
    if isprof == 1:
        judge = 1

#profileがあるとき
    if isprof == 1:
        x = []
        y = []      
        x.clear()
        y.clear()
        y_month.clear()
        z_target.clear()
        y_month = [0]
        z_target = [0]
        profile = Profile.objects.get(owner=request.user)
        data = Study.objects.filter(owner=request.user)
        data = data.filter(year=now_year, month=now_month).order_by('day').reverse()

        for d in data:
            x.append(d.day)
            y.append(d.hour)
            total += d.hour
            if d.hour > 0:
                study_day += 1

        for i in range(now_day):
            data = Study.objects.filter(owner=request.user)
            if (i+1) in x:
                month_data = data.filter(year=now_year, month=now_month, day=(i+1)).first()

                y_total += month_data.hour

            y_month.append(y_total)
            d = date(now_year, now_month, i+1)
            dd = d.weekday()
            if dd == 5 or dd == 6:
                target_total += profile.holiday_study
            else:
                target_total += profile.weekday_study
            z_target.append(target_total)
        if target_total == 0:
            rate = '0.0 %'
        else:
            rate = str(f'{(y_total / target_total) * 100:,.1f}') + '% '  

    max_hour = str(data.aggregate(Max('hour'))['hour__max'])
    if len(data) == 0:
        max_hour = 0.0
    total_hour = str(f'{total:,.1f}') 
    params = {
        'study_day': study_day,
        'max_hour': max_hour,
        'total_hour': total_hour,
        'today': today_list,
        'profile': profile,
        'target_total': target_total,
        'rate': rate,
        'judge': judge,
        'isprof': isprof,
    }
    return render(request, 'hello/index.html', params)

#グラフ作成
def setPlt(x, y, z_target, y_month):
    plt.figure(figsize=(10, 3), facecolor="#E6FFE9")
    plt.subplots_adjust(wspace=0.25)
    
    plt.subplot(1,2,1)
    plt.bar(x, y, color="coral")
    fsz = 10
    plt.rcParams["font.size"] = fsz
    plt.xlabel('days', fontsize=15)
    plt.ylabel('hour(hr)', fontsize=15)
    plt.grid(True)    
    plt.xlim([0.5, 32])

    plt.subplot(1,2,2)
    plt.plot(z_target, lw=2, label="target", linestyle = "dashed")
    plt.plot(y_month,lw=2.5, label="result", color="coral")
    plt.legend(fontsize=20)
    plt.xlabel('days', fontsize=15)
    plt.ylabel('hour(hr)', fontsize=15)
    plt.xstep = 2
    plt.grid(True)
    plt.xlim([1, 31.5])
    plt.legend(loc=2, fontsize=14)
    plt.ylim(0)

def plt2svg():
    buf = io.BytesIO()
    plt.savefig(buf, format='svg', bbox_inches='tight')
    s = buf.getvalue()
    buf.close()
    return s

def get_svg(request):
    setPlt(x, y, z_target, y_month) 
    svg = plt2svg()
    plt.cla() 
    response = HttpResponse(svg, content_type='image/svg+xml')
    return response

@login_required
def create(request):
    params = {
        'title': '記録の追加',
        'form': StudyForm(),
    }
    if (request.method == 'POST'):
        obj = Study()
        obj.owner = request.user
        study = StudyForm(request.POST, instance=obj)
        study.save()
        return redirect(to='/hello/')
    return render(request, 'hello/create.html', params)

@login_required
def create_profile(request):
    judge = 0
    isprof = Profile.objects.filter(owner=request.user).count()
    if isprof == 1:
        judge = 1
    if (request.method == 'POST'):
        obj = Profile()
        obj.owner = request.user        
        user_profile = ProfileForm(request.POST, instance=obj)
        user_profile.save()
        return redirect(to='/hello/')  
    params = {
        'title': 'あなたのプロフィール',
        'form': ProfileForm(),
        'judge': judge,
    }         
    return render(request, 'hello/create_profile.html', params)

@login_required
def edit(request, num):
    obj = Study.objects.get(id=num)
    if (request.method == 'POST'):
        study = StudyForm(request.POST, instance=obj)
        study.save()
        return redirect(to='/hello')
    params = {
        'id': num,
        'form': StudyForm(instance=obj),
    }
    return render(request, 'hello/edit.html', params)

@login_required
def edit_profile(request):
    obj = Profile.objects.get(owner=request.user)
    if (request.method == 'POST'):
        profile = ProfileForm(request.POST, instance=obj)
        profile.save()
        return redirect(to='/hello')
    params = {
        'form': ProfileForm(instance=obj),
    }
    return render(request, 'hello/edit_profile.html', params)

@login_required
def delete(request, num):
    study = Study.objects.get(id=num)
    if (request.method == 'POST'):
        study.delete()
        return redirect(to='/hello/find')
    params = {
        'title': '記録の削除',
        'id':num,
        'obj': study,
    }
    return render(request, 'hello/delete.html', params)

x = []
y = []
y_month = []
z_target = []

@login_required
def find(request):
    data = Study.objects.filter(owner=request.user)
    num_data = 0
    month_is = 0
    year=now_year
    if (request.method == 'POST'):
        year_is = 1
        msg = '検索結果'
        form = FindForm(request.POST)
        year = request.POST['find_year']
        data = Study.objects.filter(owner=request.user)
        data = data.filter(year=year).order_by('month', 'day').reverse()
        num_data = len(data)
        if num_data == 0:
            msg = '対象のデータはありません。'

        if request.POST['find_month']:
            form = FindForm(request.POST)
            month = request.POST['find_month']
            data = Study.objects.filter(owner=request.user)
            data = data.filter(month=month).order_by('day')
            num_data = len(data)
            if num_data != 0:
                month_is = 1
                global x, y
                x = []
                y = []
                x.clear()
                y.clear()
                data = Study.objects.filter(owner=request.user)
                data = data.filter(year=year, month=month).order_by('day').reverse()
                for da in data:
                    x.append(da.day)
                    y.append(da.hour) 

            elif num_data == 0:
                msg = '対象のデータはありません。'
                x.clear()
                y.clear()

    else:
        msg = '検索する年と月を入力してください。<br>※1ヶ月の推移を見るには、年、月の両方を入力して下さい。'
        form = FindForm()
        year_is = 0
        data = Study.objects.all().filter(owner=request.user)
        data = data.filter(year=now_year, month=now_month).order_by('day').reverse()

    params = {
        'message': msg,
        'form': form,
        'data': data,
        'num_data': num_data,
        'month_is': month_is,
        'year': year,
        'year_is': year_is,
    }
    return render(request, 'hello/find.html', params)

month_number = []
month_hour = []

@login_required
def all_year(request):
    global month_number, month_hour
    month_hour.clear()

    month_number = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    month_hour = []
    if (request.method == 'POST'):
        msg = '年の勉強時間データ'
        form = FindYearForm(request.POST)
        year = request.POST['find_year']
        year_stat = str(year)

    else:
        msg = '年の勉強時間データ'
        form = FindYearForm()
        year = now_year
        year_stat = '今'
     
    data = Study.objects.filter(owner=request.user)
    year_data = data.filter(year=year)
    for i in range(12):
        total = 0
        for yeardata in year_data.filter(month=i+1):
            total += yeardata.hour
        month_hour.append(total)

    params = {
        'year_stat': year_stat,
        'form': form,
        'message': msg,
    }

    return render(request, 'hello/all_year.html', params)

def bar_setPlt(x, y):
    plt.figure(figsize=(6, 3), facecolor="#E6FFE9")
    plt.bar(x, y)
    plt.title( 'transition', color='#2f4f4f', fontsize=20)
    plt.xlabel('months', fontsize=18)
    plt.ylabel('total hour(hr)', fontsize=18)
    plt.xlim([0.1, 12.5])
    plt.ylim(0.3)
    plt.xticks( np.arange(1, 13, 1) )
    
def bar_plt2svg():
    buf = io.BytesIO()
    plt.savefig(buf, format='svg', bbox_inches='tight')
    s = buf.getvalue()
    buf.close()
    return s

def get_bar_svg(request):
    bar_setPlt(month_number, month_hour) 
    svg = bar_plt2svg()
    plt.cla() 
    response = HttpResponse(svg, content_type='image/svg+xml')
    return response

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)        
        if form.is_valid():
            form.save()
            return redirect('hello:index')
    else:
        form = SignUpForm()

    context = {'form':form}
    return render(request, 'hello/signup.html', context)

def all_users(request):

    #プロフィール欄の部分を取得
    profile_data = Profile.objects.order_by('owner_id')    

    profile_list = []
    profile_list.clear()
    for data in profile_data:
        profile_list.append(data.id)

    #各ユーザーの今日の勉強時間を取得
    today_study_list = []
    today_study_list.clear()
    for profile_id in profile_list:
        studydata = Study.objects.filter(owner_id=profile_id)     
        #今日の勉強時間を取得
        study_data_count = studydata.filter(day=now_day).count()
        if study_data_count >= 1:
            studydata = studydata.filter(day=now_day).first()
            today_study_list.append(studydata.hour)
        else:
            today_study_list.append(0.0)

    today_study_target_list = []    
    today_study_target_list.clear()
    for profile_id in profile_list:
        profile = Profile.objects.get(owner_id=profile_id)
        d = date(now_year, now_month, now_day)
        dd = d.weekday()
        if dd == 5 or dd == 6:
            target_hour = profile.holiday_study
            today_study_target_list.append(target_hour)

        else:
            target_hour = profile.weekday_study
            today_study_target_list.append(target_hour)
    
    profile_data = Profile.objects.all()
    #templatesでpopで逆順に取り出すため
    today_study_target_list.reverse()
    today_study_list.reverse()

    context = {
        'data': data,
        #'profile_list': profile_list,
        'profile_data': profile_data,
        'today_study_target_list': today_study_target_list,
        'today_study_list': today_study_list,
        }
    return render(request, 'hello/all_users.html', context)