from django.db import models

# Create your models here.

class Username(models.Model):
    user = models.CharField(max_length=100)
    email = models.CharField(max_length=100)

    def __str__(self):
        return self.user