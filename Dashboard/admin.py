from django.contrib import admin
from .models import Linksinfo,ViewLinksData
# Register your models here.
# admin.site.register(Linksinfo)
@admin.register(Linksinfo)
class Linksadmin(admin.ModelAdmin):
    list_display = ['id','uid','pid','ip','status','systemTime','completionTime']

@admin.register(ViewLinksData)
class ProxyView(admin.ModelAdmin):
    list_display = ['id','uid','pid','ip','status','systemTime','completionTime']