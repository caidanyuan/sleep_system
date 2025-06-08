from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class SleepRecord(models.Model):
    SLEEP_QUALITY_CHOICES = [
        (1, '非常差'),
        (2, '差'),
        (3, '一般'),
        (4, '好'),
        (5, '非常好'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    bedtime = models.TimeField()
    wakeup_time = models.TimeField()
    sleep_duration = models.FloatField(help_text="小时")
    sleep_quality = models.IntegerField(choices=SLEEP_QUALITY_CHOICES)
    deep_sleep_percentage = models.FloatField(help_text="深度睡眠百分比")
    rem_sleep_percentage = models.FloatField(help_text="快速眼动睡眠百分比")
    awakenings = models.IntegerField(help_text="夜间醒来次数")
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.date}"


class SleepGoal(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    target_bedtime = models.TimeField()
    target_wakeup_time = models.TimeField()
    target_sleep_duration = models.FloatField(help_text="目标睡眠时长(小时)")

    def __str__(self):
        return f"{self.user.username} 的睡眠目标"


class CommunityPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(CommunityPost, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}对'{self.post.title}'的评论"