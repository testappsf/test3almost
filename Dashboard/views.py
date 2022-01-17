from django.db.models.fields import DateTimeField
from django.http import HttpResponseRedirect
from django.shortcuts import render,HttpResponse
from .models import Linksinfo,ViewLinksData
from .forms import punches
import datetime
from django.db.models import Q
from django.core.paginator import Paginator
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
            link.uid = uid
            link.pid= pid
            link.ip = ip
            link.systemTime= systemTime
            link.completionTime= completionTime
            link.status = status
            link.save()
            return render(request,'dashboard/terminate.html',{'UID':uid,'PID':pid,'IP':ip,'sys':systemTime,'comt':completionTime,'STATUS':status})
        else:
            return HttpResponse('<h1> form is valid but unable to punch</h1>')
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

            if(checkippid(pid,ip) == True):
                return HttpResponse("<h1> Same IP found </h1>")
            # if (check!=True):
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
            return HttpResponse('<h1> form is valid but unable to punch</h1>')
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
            link.uid = uid
            link.pid= pid
            link.ip = ip
            link.systemTime= systemTime
            link.completionTime= completionTime
            link.status = status
            link.save()
            print('uid:',fm.cleaned_data['uid'])
            print('pid:',fm.cleaned_data['pid'])
            print(systemTime)
            print(completionTime)
            print(status)
            print(get_client_ip(request));
            return render(request,'dashboard/terminate.html',{'UID':uid,'PID':pid,'IP':ip,'sys':systemTime,'comt':completionTime,'STATUS':status})
        else:
            return HttpResponse('<h1> form is valid but unable to punch</h1>')
    else:
        return HttpResponse('<h1>Something went Wrong</h1>')

# def viewDashboard(request):
#     # if request.method == 'POST':
#     #     fm = request.
#     #     if form.is_valid:

#     links = ViewLinksData.objects.order_by("id").distinct()
#     return render(request,'dashboard/dashboard.html',{'links':links})


def checkippid(pid,ip):
    linkcheck= Linksinfo.objects.filter(Q(pid__iexact=pid) & Q(ip=ip))
    return linkcheck.exists()

def viewDashboard(request):
    qs = ViewLinksData.objects.all().distinct()
    if request.method =="POST" :
        P_id = request.POST.get('p_id')
        U_id = request.POST.get('u_id')
        if(P_id !='' and P_id is not None):
            qs = qs.filter(Q(pid__exact=P_id) | Q(pid__iexact=P_id) | Q(pid__icontains =P_id)).distinct()
        if(U_id !='' and U_id is not None):
            qs = qs.filter(Q(uid__iendswith=U_id)).distinct()
    
    paginator= Paginator(qs,100,orphans=1)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    return render(request,'dashboard/dashboard.html',{'page_obj':page_obj})