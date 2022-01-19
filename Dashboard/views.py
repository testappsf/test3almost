from django.http import HttpResponseRedirect, response
from django.shortcuts import render,HttpResponse
from .models import Linksinfo,ViewLinksData
from .forms import punches
import datetime
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
import csv

# Create your views here.
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    print(x_forwarded_for)
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
    
def home(request):
    return render(request,'home.html')
    
def terminate(request):
    if request.method =='GET':
        fm = punches(request.GET)
        link = Linksinfo()
        if fm.is_valid():
            print('form validated')
            uid = fm.cleaned_data['uid']
            pid = fm.cleaned_data['pid']
            ip = get_client_ip(request)
            systemTime = datetime.datetime.today()
            completionTime= datetime.datetime.now()
            status = 'Terminate'
            if(checkippid(uid,ip) == True):
                return HttpResponse("<h1> Same IP found </h1>")
            else:
                link.uid = uid
                link.pid= pid
                link.ip = ip
                link.systemTime= systemTime
                link.completionTime= completionTime
                link.status = status
                link.save()
                return render(request,'dashboard/terminate.html',{'UID':uid,'PID':pid,'IP':ip,'sys':systemTime,'comt':completionTime,'STATUS':status})
        else:
            return HttpResponse('<h1> Invalid Data</h1>')
    else:
        return HttpResponse('<h1>Something went Wrong</h1>')


def complete(request):
    if request.method =='GET':
        fm = punches(request.GET)
        link = Linksinfo()
        if fm.is_valid():
            print('form validated')
            uid = fm.cleaned_data['uid']
            pid = fm.cleaned_data['pid']
            ip = get_client_ip(request)
            systemTime = datetime.datetime.today()
            completionTime= datetime.datetime.today()

            if(checkippid(uid,ip) == True):
                return HttpResponse("<h1> Same IP found </h1>")
            else:
                status = 'complete'
                link.uid = uid
                link.pid= pid
                link.ip = ip
                link.systemTime= systemTime
                link.completionTime= completionTime
                link.status = status
                link.save()
                return render(request,'dashboard/terminate.html',{'UID':uid,'PID':pid,'IP':ip,'sys':systemTime,'comt':completionTime,'STATUS':status})
        else:
            return HttpResponse('<h1> Invalid data</h1>')
    else:
        return HttpResponse('<h1>Something went Wrong</h1>')

def quotafull(request):
    if request.method =='GET':
        fm = punches(request.GET)
        link = Linksinfo()
        if fm.is_valid():
            print('form validated')
            uid = fm.cleaned_data['uid']
            pid = fm.cleaned_data['pid']
            ip = get_client_ip(request)
            systemTime = datetime.datetime.today()
            completionTime= datetime.datetime.today()
            status = 'QuotaFull'
            if(checkippid(uid,ip) == True):
                return HttpResponse("<h1> Same IP found </h1>")
            else:
                link.uid = uid
                link.pid= pid
                link.ip = ip
                link.systemTime= systemTime
                link.completionTime= completionTime
                link.status = status
                link.save()
                return render(request,'dashboard/terminate.html',{'UID':uid,'PID':pid,'IP':ip,'sys':systemTime,'comt':completionTime,'STATUS':status})
        else:
            return HttpResponse('<h1> Invalid data</h1>')
    else:
        return HttpResponse('<h1>Something went Wrong</h1>')

def checkippid(pid,ip):
    linkcheck= Linksinfo.objects.filter(Q(uid__iexact=pid) & Q(ip=ip))
    return linkcheck.exists()

@login_required
def viewDashboard(request):
    qs = ViewLinksData.objects.all().distinct()
    if request.method =="POST" :
        P_id = request.POST.get('p_id')
        U_ide = request.POST.get('u_ide')
        U_ids = request.POST.get('u_ids')
        status = request.POST.get('status')
        compltime = request.POST.get('date')
        if(P_id !='' and P_id is not None):
            print("works pid")
            qs = qs.filter(Q(pid__exact=P_id) | Q(pid__iexact=P_id) | Q(pid__icontains=P_id)).distinct()
        if(U_ide !='' and U_ide is not None):
            print("works uide")
            qs = qs.filter(Q(uid__iendswith=U_ide)).distinct()
        if(U_ids !='' and U_ids is not None):
            print("work uids")
            qs = qs.filter(Q(uid__istartswith=U_ids)).distinct()
        if(status !='' and status is not None):
            print(" work status")
            qs = qs.filter(Q(status__iexact=status)).distinct()
        if(compltime !='' and compltime is not None):
            print(compltime)
            qs = qs.filter(Q(completionTime__date__gte=compltime)).distinct()
    
    paginator= Paginator(qs,100,orphans=1)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    return render(request,'dashboard/dashboard1.html',{'page_obj':page_obj})


def export_csv(request):
    response=HttpResponse(content_type="text/csv")
    response['content-Disposition']= 'attachment; filename=linksdata' +'.csv'
    writer = csv.writer(response)
    writer.writerow(['Project Id','user_id','status','datetime'])
    vdata = ViewLinksData.objects.all()

    for data in vdata:
        writer.writerow([data.pid,data.uid,data.status,data.completionTime])

    return response