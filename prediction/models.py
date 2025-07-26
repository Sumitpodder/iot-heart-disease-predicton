from django.db import models
from django.utils import timezone

class HealthRecord(models.Model):
    name=models.CharField(max_length=20,default="Unknown")
    age = models.IntegerField()
    gender=models.CharField(max_length=6,default='M')
    cp = models.IntegerField(choices=[(0, 'High'), (1, 'Medium'), (2, 'Low'), (3, 'None')])
    trestbps=models.IntegerField(default=120)
    chol=models.IntegerField(default=250)
    thalach = models.IntegerField()
    oldpeak = models.FloatField()
    heartrate=models.IntegerField(default=72)
    spo2=models.IntegerField(default=95)
    ca = models.IntegerField(choices=[(0, 'None'), (1, 'Low'), (2, 'Medium'), (3, 'High'),(4,'Extreme')])
    thal = models.IntegerField(choices=[(0, 'Unknown'), (1, 'Low'), (2, 'Medium'), (3, 'High')])
    timestamp = models.DateTimeField(default=timezone.now)

    result= models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name} - {self.result}"


    