from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    # public pages - no login needed
    path('', views.task_list, name='task_list'),
    path('<int:pk>/', views.task_detail, name='task_detail'),
    # client actions
    path('post/', views.post_task, name='post_task'),
    path('<int:pk>/edit/', views.edit_task, name='edit_task'),
    path('<int:pk>/cancel/', views.cancel_task, name='cancel_task'),
    # dashboards
    path('dashboard/client/', views.client_dashboard, name='client_dashboard'),
    path('dashboard/freelancer/', views.freelancer_dashboard, name='freelancer_dashboard'),
]
