from math import pi
from django.db.models.fields import DateTimeField
from django.shortcuts import render,HttpResponse
from .models import Linksinfo
from .forms import punches
import datetime
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
            print('form validated');
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
            print('uid:',fm.cleaned_data['uid'])
            print('pid:',fm.cleaned_data['pid'])
            print(systemTime)
            print(completionTime)
            print(status)
            print(get_client_ip(request));
            return render(request,'dashboard/terminate.html',{'UID':uid,'PID':pid,'IP':ip,'sys':systemTime,'comt':completionTime})
        else:
            return HttpResponse('<h1> form is valid but unable to punch</h1>')
    else:
        return HttpResponse('<h1>Something went Wrong</h1>')


