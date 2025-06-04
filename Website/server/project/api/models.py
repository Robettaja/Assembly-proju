from django.db import models

# Create your models here.

class Username(models.Model):
    user = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    laptime = models.CharField(max_length=20, blank =True, null=True)

    def __str__(self):
        return self.user