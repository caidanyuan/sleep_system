from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import SleepRecord, SleepGoal, CommunityPost, Comment
from .forms import SleepRecordForm, SleepGoalForm, CommunityPostForm, CommentForm
from datetime import datetime, timedelta
import random


def index(request):
    return render(request, 'sleepapp/index.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'sleepapp/login.html', {'error': '用户名或密码错误'})
    return render(request, 'sleepapp/login.html')


def logout_view(request):
    logout(request)
    return redirect('index')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'sleepapp/register.html', {'form': form})


@login_required
def sleep_analysis(request):
    # 获取最近7天的睡眠记录
    records = SleepRecord.objects.filter(user=request.user).order_by('-date')[:7]

    # 计算平均睡眠质量
    avg_quality = records.aggregate(models.Avg('sleep_quality'))['sleep_quality__avg'] or 0

    # 生成睡眠改善建议
    recommendations = generate_recommendations(records)

    context = {
        'records': records,
        'avg_quality': round(avg_quality, 1),
        'recommendations': recommendations
    }
    return render(request, 'sleepapp/sleep_analysis.html', context)


@login_required
def monitoring_data(request):
    records = SleepRecord.objects.filter(user=request.user).order_by('-date')
    context = {'records': records}
    return render(request, 'sleepapp/monitoring_data.html', context)


@login_required
def trend_prediction(request):
    # 模拟预测数据（实际项目中应使用真实预测模型）
    today = datetime.now().date()
    dates = [today + timedelta(days=i) for i in range(7)]
    predicted_quality = [random.uniform(3.0, 4.5) for _ in range(7)]

    context = {
        'dates': dates,
        'predicted_quality': predicted_quality
    }
    return render(request, 'sleepapp/trend_prediction.html', context)


@login_required
def community(request):
    posts = CommunityPost.objects.all().order_by('-created_at')
    context = {'posts': posts}
    return render(request, 'sleepapp/community.html', context)


@login_required
def settings_view(request):
    try:
        goal = SleepGoal.objects.get(user=request.user)
    except SleepGoal.DoesNotExist:
        goal = None

    if request.method == 'POST':
        form = SleepGoalForm(request.POST, instance=goal)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            return redirect('settings')
    else:
        form = SleepGoalForm(instance=goal)

    context = {'form': form}
    return render(request, 'sleepapp/settings.html', context)


def help_center(request):
    faqs = [
        {"question": "如何添加睡眠记录？", "answer": "在'监控数据'页面点击'添加记录'按钮，填写相关信息后提交。"},
        {"question": "睡眠质量评分是如何计算的？", "answer": "睡眠质量评分基于多个因素，包括睡眠时长、深度睡眠比例、醒来次数等。"},
        {"question": "如何设置睡眠目标？", "answer": "在'系统设置'页面可以设置您的睡眠目标。"},
        {"question": "趋势预测是如何工作的？", "answer": "系统根据您过去的睡眠数据和习惯，使用机器学习算法预测未来睡眠质量趋势。"},
    ]
    context = {'faqs': faqs}
    return render(request, 'sleepapp/help_center.html', context)


@login_required
def add_sleep_record(request):
    if request.method == 'POST':
        form = SleepRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.user = request.user
            record.save()
            return redirect('monitoring_data')
    else:
        form = SleepRecordForm()

    context = {'form': form}
    return render(request, 'sleepapp/add_sleep_record.html', context)


@login_required
def post_detail(request, post_id):
    post = CommunityPost.objects.get(id=post_id)
    comments = Comment.objects.filter(post=post).order_by('created_at')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'form': form
    }
    return render(request, 'sleepapp/post_detail.html', context)


def generate_recommendations(records):
    if not records:
        return ["请添加睡眠记录以获取个性化建议"]

    latest_record = records[0]
    recommendations = []

    # 基于睡眠时长建议
    if latest_record.sleep_duration < 7:
        recommendations.append("您的睡眠时长可能不足，建议增加睡眠时间至7-9小时。")
    elif latest_record.sleep_duration > 9:
        recommendations.append("您的睡眠时长可能过长，建议控制在7-9小时之间。")

    # 基于睡眠质量建议
    if latest_record.sleep_quality < 3:
        recommendations.append("您的睡眠质量较低，建议保持规律的睡眠时间表。")

    # 基于深度睡眠比例建议
    if latest_record.deep_sleep_percentage < 20:
        recommendations.append("深度睡眠比例较低，建议睡前避免蓝光设备使用。")

    # 基于醒来次数建议
    if latest_record.awakenings > 2:
        recommendations.append("夜间醒来次数较多，建议减少晚间液体摄入。")

    if not recommendations:
        recommendations.append("您的睡眠习惯良好！继续保持！")

    return recommendations