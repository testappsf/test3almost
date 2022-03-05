
from unicodedata import name
from django.urls import path
from .views import surveydata,viewDashboard,export_csv,user_profile
urlpatterns = [
    path('terminate/', surveydata,{'check':'terminate'}),
    path('quotafull/',surveydata,{'check':'quotafull'}),
    path('complete/',surveydata,{'check':'complete'}),
    path('profile/',viewDashboard,name='dashboard'),
    path('dashboard/filter/',filter),
    path('profile-changes/',user_profile,name='profile'),
    path('profile/export',export_csv,name='export-csv'),
    
]
