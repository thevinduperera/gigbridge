from django.urls import path
from . import views
app_name = 'proposals'
urlpatterns = [
    path('submit/<int:task_id>/', views.submit_proposal, name='submit_proposal'),
    path('mine/', views.my_proposals, name='my_proposals'),
    path('task/<int:task_id>/', views.view_proposals, name='view_proposals'),
    path('award/<int:proposal_id>/', views.award_proposal, name='award_proposal'),
    path('reject/<int:proposal_id>/', views.reject_proposal, name='reject_proposal'),
    path('complete/<int:task_id>/', views.mark_completed, name='mark_completed'),
    path('review/<int:proposal_id>/', views.leave_review, name='leave_review'),
    path('detail/<int:proposal_id>/', views.proposal_detail, name='proposal_detail'),
    path('task/<int:task_id>/', views.task_proposals, name='task_proposals'),
    path('award/<int:proposal_id>/', views.award_proposal, name='award_proposal'),
    path('reject/<int:proposal_id>/', views.reject_proposal, name='reject_proposal'),
]
