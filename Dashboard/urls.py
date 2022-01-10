
from django.urls import path
from .views import terminate

urlpatterns = [
    path('terminate/', terminate),
]
