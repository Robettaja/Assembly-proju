from django.db import models

# Create your models here.

class Username(models.Model):
    user = models.CharField(max_length=100)
    
    lap1 = models.CharField(max_length=20, blank=True, null=True)
    lap2 = models.CharField(max_length=20, blank=True, null=True)
    lap3 = models.CharField(max_length=20, blank=True, null=True)


    total_time = models.CharField(max_length=20, blank =True, null=True)

    def __str__(self):
        return self.user