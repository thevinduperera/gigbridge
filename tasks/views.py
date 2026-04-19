# tasks/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Task, Category, Skill
from .forms import TaskForm


@login_required
def post_task(request):
    # clients only - freelancers shouldn't be posting tasks
    if getattr(request.user, 'role', None) != 'client':
        messages.error(request, "Only clients can post tasks.")
        return redirect('core:home')

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            # commit=False lets us attach the client before hitting the database
            task = form.save(commit=False)
            task.client = request.user
            task.save()
            # save_m2m() is needed here because we used commit=False above
            # otherwise the skills won't get saved
            form.save_m2m()
            messages.success(request, "Your task has been posted successfully!")
            return redirect('tasks:task_detail', pk=task.pk)
    else:
        form = TaskForm()

    return render(request, 'tasks/post_task.html', {'form': form})


def task_list(request):
    # open to everyone, no login needed
    tasks      = Task.objects.filter(status='open').select_related('category', 'client')
    categories = Category.objects.all()

    # handle search
    query = request.GET.get('q')
    if query:
        tasks = tasks.filter(title__icontains=query)

    # handle category filter
    category_slug = request.GET.get('category')
    if category_slug:
        tasks = tasks.filter(category__slug=category_slug)

    # handle budget filter
    budget_min = request.GET.get('budget_min')
    budget_max = request.GET.get('budget_max')
    if budget_min:
        tasks = tasks.filter(budget_max__gte=budget_min)
    if budget_max:
        tasks = tasks.filter(budget_min__lte=budget_max)

    context = {
        'tasks':         tasks,
        'categories':    categories,
        'query':         query,
        'category_slug': category_slug,
        'budget_min':    budget_min,
        'budget_max':    budget_max,
    }
    return render(request, 'tasks/task_list.html', context)


def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'tasks/task_detail.html', {'task': task})


@login_required
def edit_task(request, pk):
    task = get_object_or_404(Task, pk=pk)

    # stop anyone other than the owner from editing
    if request.user != task.client:
        messages.error(request, "You are not allowed to edit this task.")
        return redirect('tasks:task_detail', pk=task.pk)

    # no point editing a task that's already underway
    if not task.is_open():
        messages.error(request, "You can only edit tasks that are still open.")
        return redirect('tasks:task_detail', pk=task.pk)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task updated successfully!")
            return redirect('tasks:task_detail', pk=task.pk)
    else:
        # pre-fill the form with the existing task data
        form = TaskForm(instance=task)

    return render(request, 'tasks/edit_task.html', {'form': form, 'task': task})


@login_required
def cancel_task(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.user != task.client:
        messages.error(request, "You are not allowed to cancel this task.")
        return redirect('tasks:task_detail', pk=task.pk)

    if not task.is_open():
        messages.error(request, "Only open tasks can be cancelled.")
        return redirect('tasks:task_detail', pk=task.pk)

    if request.method == 'POST':
        task.status = Task.STATUS_CANCELLED
        task.save()
        messages.success(request, "Task has been cancelled.")
        return redirect('tasks:client_dashboard')

    return redirect('tasks:task_detail', pk=task.pk)


@login_required
def client_dashboard(request):
    if getattr(request.user, 'role', None) != 'client':
        messages.error(request, "Access denied.")
        return redirect('core:home')

    tasks = Task.objects.filter(client=request.user).select_related('category')

    context = {
        'tasks':             tasks,
        'total_tasks':       tasks.count(),
        'open_tasks':        tasks.filter(status='open').count(),
        'in_progress_tasks': tasks.filter(status='in_progress').count(),
        'completed_tasks':   tasks.filter(status='completed').count(),
    }
    return render(request, 'tasks/client_dashboard.html', context)


@login_required
def freelancer_dashboard(request):
    if getattr(request.user, 'role', None) != 'freelancer':
        messages.error(request, "Access denied.")
        return redirect('core:home')

    # submitted_proposals comes from related_name in Member 3's Proposal model
    proposals = request.user.submitted_proposals.all().select_related('task')

    context = {
        'proposals':          proposals,
        'total_proposals':    proposals.count(),
        'pending_proposals':  proposals.filter(status='pending').count(),
        'accepted_proposals': proposals.filter(status='accepted').count(),
        'rejected_proposals': proposals.filter(status='rejected').count(),
    }
    return render(request, 'tasks/freelancer_dashboard.html', context)