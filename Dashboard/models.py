from django.db import models

# Create your models here.

class Linksinfo(models.Model):
    uid = models.CharField(max_length=40)
    pid = models.CharField(max_length=40)
    ip = models.CharField(max_length=20)
    status=models.CharField(max_length=10)
    systemTime = models.DateTimeField(auto_now=False,auto_now_add=True)
    completionTime= models.DateTimeField(auto_now=False)


    def __str__(self):
        return self.uid