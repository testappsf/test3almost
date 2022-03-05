
from django.http import HttpResponseRedirect
from django.shortcuts import render,HttpResponse
from .models import Linksinfo,ViewLinksData
from .forms import punches
import datetime
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
import csv
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm,PasswordChangeForm,UserChangeForm
from .forms import Edituserprofileform,EditAdminprofileform

# Create your views here.

def error_404_view(request,exception):
    return render(request,'error.html')

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    print(x_forwarded_for)
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
    
def home(request):
    return render(request,'blog/home.html')
    
def checkippid(uid,ip,pid):
    linkcheck= Linksinfo.objects.filter((Q(pid__iexact=pid) & Q(ip=ip)) |(Q(pid__exact=pid) & Q(uid__exact=uid)))
    print(linkcheck)
    return linkcheck.exists()

@login_required
def viewDashboard(request):
    qs = ViewLinksData.objects.all().distinct()
    if request.method =="POST" :
        Univ = request.POST.get('uni')
        P_id = request.POST.get('p_id')
        U_ide = request.POST.get('u_ide')
        U_ids = request.POST.get('u_ids')
        status = request.POST.get('status')
        compltime = request.POST.get('date')
        if(Univ !='' and Univ is not None):
            qs=qs.filter(Q(pid__icontains=Univ)|Q(uid__icontains=Univ)| \
                Q(status__icontains=Univ) |Q(completionTime__icontains=Univ))
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
    return render(request,'dashboard/dashboard.html',{'page_obj':page_obj})

@login_required
def export_csv(request):
    response=HttpResponse(content_type="text/csv")
    response['content-Disposition']= 'attachment; filename=linksdata' +'.csv'
    writer = csv.writer(response)
    writer.writerow(['Project Id','user_id','status','datetime'])
    vdata = ViewLinksData.objects.all()

    for data in vdata:
        writer.writerow([data.pid,data.uid,data.status,data.completionTime])
    return response


def surveydata(request,check):
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
            status = check
            if(checkippid(uid,ip,pid) == True):
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

def user_profile(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            if request.user.is_superuser==True:
                fm=EditAdminprofileform(instance=request.user)
            else:
                fm=Edituserprofileform(request.POST,instance=request.user)
            if fm.is_valid():
                messages.success(request,'Profile Updated !!!')
                fm.save()
        else:
            if request.user.is_superuser==True:
                fm=EditAdminprofileform(instance=request.user)
            else:   
                fm=Edituserprofileform(instance=request.user)
        return render(request,'registration/profile.html', {'name':request.user.username,'form':fm})
    else:
        return HttpResponseRedirect('/login/')