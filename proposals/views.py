from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Proposal, Review
from .forms import ProposalForm, RejectForm, ReviewForm

@login_required
def submit_proposal(request, task_id):
    from tasks.models import Task
    task = get_object_or_404(Task, id=task_id)
    # Check if freelancer already applied
    already_applied = Proposal.objects.filter(
        task=task, freelancer=request.user
    ).exists()
    if already_applied:
        messages.warning(request, 'You have already applied for this task!')
        return redirect('task_detail', pk=task_id)
    if request.method == 'POST':
        form = ProposalForm(request.POST)
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.task = task
            proposal.freelancer = request.user
            proposal.save()
            messages.success(request, 'Proposal submitted!')
            return redirect('task_detail', pk=task_id)
    else:
        form = ProposalForm()
    return render(request, 'proposals/submit_proposal.html',
                  {'form': form, 'task': task})

@login_required
def my_proposals(request):
    proposals = Proposal.objects.filter(
        freelancer=request.user
    ).select_related('task')
    status_filter = request.GET.get('status', '')
    search = request.GET.get('search', '')
    if status_filter:
        proposals = proposals.filter(status=status_filter)
    if search:
        proposals = proposals.filter(task__title__icontains=search)
    return render(request, 'proposals/my_proposals.html',
                  {'proposals': proposals,
                   'status_filter': status_filter,
                   'search': search})
@login_required
def view_proposals(request, task_id):
    from tasks.models import Task
    task = get_object_or_404(Task, id=task_id, client=request.user)
    proposals = task.proposals.select_related('freelancer')
    return render(request, 'proposals/view_proposals.html',
                  {'task': task, 'proposals': proposals})

@login_required
def award_proposal(request, proposal_id):
    proposal = get_object_or_404(Proposal, id=proposal_id)
    proposal.status = 'awarded'
    proposal.save()
    proposal.task.status = 'in_progress'
    proposal.task.save()
    messages.success(request, 'Task awarded successfully!')
    return redirect('view_proposals', task_id=proposal.task.id)

@login_required
def reject_proposal(request, proposal_id):
    proposal = get_object_or_404(Proposal, id=proposal_id)
    if request.method == 'POST':
        form = RejectForm(request.POST)
        if form.is_valid():
            proposal.status = 'rejected'
            proposal.reject_reason = form.cleaned_data['reason']
            proposal.save()
            messages.info(request, 'Proposal rejected.')
            return redirect('view_proposals', task_id=proposal.task.id)
    else:
        form = RejectForm()
    return render(request, 'proposals/reject_proposal.html',
                  {'form': form, 'proposal': proposal})

@login_required
def mark_completed(request, task_id):
    from tasks.models import Task
    task = get_object_or_404(Task, id=task_id, client=request.user)
    task.status = 'completed'
    task.save()
    awarded = task.proposals.filter(status='awarded').first()
    return render(request, 'proposals/leave_review.html',
                  {'task': task, 'proposal': awarded,
                   'form': ReviewForm()})

@login_required
def leave_review(request, proposal_id):
    proposal = get_object_or_404(Proposal, id=proposal_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.proposal = proposal
            review.save()
            messages.success(request, 'Review saved!')
            return redirect('my_proposals')
    return redirect('my_proposals')

@login_required
def proposal_detail(request, proposal_id):
    proposal = get_object_or_404(
        Proposal, id=proposal_id, freelancer=request.user
    )
    return render(request, 'proposals/proposal_detail.html',
                  {'proposal': proposal})