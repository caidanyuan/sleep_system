from django import forms
from .models import SleepRecord, SleepGoal, CommunityPost, Comment

class SleepRecordForm(forms.ModelForm):
    class Meta:
        model = SleepRecord
        fields = ['date', 'bedtime', 'wakeup_time', 'sleep_quality',
                  'deep_sleep_percentage', 'rem_sleep_percentage',
                  'awakenings', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'bedtime': forms.TimeInput(attrs={'type': 'time'}),
            'wakeup_time': forms.TimeInput(attrs={'type': 'time'}),
        }

class SleepGoalForm(forms.ModelForm):
    class Meta:
        model = SleepGoal
        fields = ['target_bedtime', 'target_wakeup_time', 'target_sleep_duration']
        widgets = {
            'target_bedtime': forms.TimeInput(attrs={'type': 'time'}),
            'target_wakeup_time': forms.TimeInput(attrs={'type': 'time'}),
        }

class CommunityPostForm(forms.ModelForm):
    class Meta:
        model = CommunityPost
        fields = ['title', 'content']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']