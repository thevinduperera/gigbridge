from django.urls import path
from .views import (
    public_freelancer_profile_view,
    register_view,
    login_view,
    logout_view,
    freelancer_profile_edit_view,
    freelancer_profile_view,
)

app_name = 'accounts'

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('freelancer/profile/edit/', freelancer_profile_edit_view, name='freelancer_profile_edit'),
    path('freelancer/profile/', freelancer_profile_view, name='freelancer_profile_view'),
    path('freelancer/<str:username>/', public_freelancer_profile_view, name='public_freelancer_profile'),
]