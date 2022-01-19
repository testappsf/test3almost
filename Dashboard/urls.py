
from unicodedata import name
from django.urls import path
from .views import terminate,quotafull,complete,viewDashboard,export_csv

urlpatterns = [
    # path('terminate/', terminate),
    # path('quotafull/',quotafull),
    # path('complete/',complete),
    path('profile/',viewDashboard),
    # path('dashboard/filter/',filter),
    path('profile/export',export_csv,name='export-csv')
    
]
