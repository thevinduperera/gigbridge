from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Notification


def home(request):
    context = {}
    return render(request, 'core/home.html', context)


def browse_tasks(request):
    return render(request, 'core/browse_tasks.html', {})


def browse_freelancers(request):
    return render(request, 'core/browse_freelancers.html', {})


@login_required
def notifications(request):
    notifs = Notification.objects.filter(recipient=request.user)
    unread_count = notifs.filter(is_read=False).count()
    return render(request, 'core/notifications.html', {
        'notifications': notifs,
        'unread_count': unread_count,
    })


@login_required
def mark_all_read(request):
    Notification.objects.filter(
        recipient=request.user, is_read=False
    ).update(is_read=True)
    messages.success(request, 'All notifications marked as read.')
    return redirect('core:notifications')