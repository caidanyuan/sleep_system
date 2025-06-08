from django.db import models
from django.contrib.auth.models import User

class SleepRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    duration = models.FloatField()  # 小时
    quality = models.IntegerField()  # 1-10分
    heart_rate = models.IntegerField()  # 平均心率
    movement = models.IntegerField()  # 翻身次数
    notes = models.TextField(blank=True)

class SleepPrediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prediction_date = models.DateField()
    predicted_quality = models.FloatField()