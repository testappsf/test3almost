
from django.urls import path
from .views import terminate,quotafull,complete,viewDashboard

urlpatterns = [
    path('terminate/', terminate),
    path('quotafull/',quotafull),
    path('complete/',complete),
    path('dashboard/',viewDashboard),
    # path('dashboard/filter/',filter),
]
