from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('tasks/', views.browse_tasks, name='browse_tasks'),
    path('freelancers/', views.browse_freelancers, name='browse_freelancers'),
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/mark-all/', views.mark_all_read, name='mark_all_read'),
]