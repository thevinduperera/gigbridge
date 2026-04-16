from django.urls import path
from .views import (
    register_view,
    login_view,
    client_dashboard,
    freelancer_dashboard,
    logout_view
)

app_name = 'accounts'

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('client-dashboard/', client_dashboard, name='accounts_client_dashboard'),
    path('freelancer-dashboard/', freelancer_dashboard, name='accounts_freelancer_dashboard'),
    path('logout/', logout_view, name='logout'),
]