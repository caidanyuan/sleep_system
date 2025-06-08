from django.urls import path
from . import views

app_name = 'sleepapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('sleep-analysis/', views.sleep_analysis, name='sleep_analysis'),
    path('monitoring-data/', views.monitoring_data, name='monitoring_data'),
    path('trend-prediction/', views.trend_prediction, name='trend_prediction'),
    path('community/', views.community, name='community'),
    path('settings/', views.settings_view, name='settings'),
    path('help-center/', views.help_center, name='help_center'),
    path('add-sleep-record/', views.add_sleep_record, name='add_sleep_record'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('add-comment/<int:post_id>/', views.add_comment, name='add_comment'),
]