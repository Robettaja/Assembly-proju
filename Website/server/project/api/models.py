from django.db import models

# Create your models here.

# class Username(models.Model):
#     user = models.CharField(max_length=100)
    
#     lap1 = models.CharField(max_length=20, blank=True, null=True)
#     lap2 = models.CharField(max_length=20, blank=True, null=True)
#     lap3 = models.CharField(max_length=20, blank=True, null=True)


#     total_time = models.CharField(max_length=20, blank =True, null=True)

#     def __str__(self):
#         return self.user

class Username(models.Model):
    user = models.CharField(max_length=100)
    total_time = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.user
    
class RaceSession(models.Model):
    user = models.ForeignKey(Username, on_delete=models.CASCADE, related_name='race_sessions')
    total_time = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.user} - Session {self.id} at {self.created_at}"

class LapTime(models.Model):
    user = models.ForeignKey(Username, on_delete=models.CASCADE, related_name='lap_times')
    lap_number = models.IntegerField()
    lap_time = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user.user} - Lap {self.lap_number}: {self.lap_time}"