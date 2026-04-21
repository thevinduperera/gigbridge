from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Notification
from accounts.models import User
from django.db.models import Q


def home(request):
    context = {}
    return render(request, 'core/home.html', context)


def browse_tasks(request):
    return render(request, 'core/browse_tasks.html', {})



def browse_freelancers(request):
    query = request.GET.get('q', '')

    freelancers = User.objects.filter(role='freelancer')

    if query:
        freelancers = freelancers.filter(
            Q(username__icontains=query) |
            Q(headline__icontains=query) |
            Q(skills__icontains=query) |
            Q(availability__icontains=query)
        )

    return render(request, 'core/browse_freelancers.html', {
        'freelancers': freelancers,
        'query': query,
    })


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

def handler404(request, exception):
    return render(request, '404.html', status=404)


def handler500(request):
    return render(request, '500.html', status=500)