from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Proposal, Review
from .forms import ProposalForm, RejectForm, ReviewForm
from tasks.models import Task
from django.db import transaction

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
        return redirect('tasks:task_detail', pk=task.id)
    if request.method == 'POST':
        form = ProposalForm(request.POST)
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.task = task
            proposal.freelancer = request.user
            proposal.save()
            messages.success(request, 'Proposal submitted!')
            return redirect('tasks:task_detail', pk=task.id)
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
def task_proposals(request, task_id):
    from tasks.models import Task
    task = get_object_or_404(Task, id=task_id, client=request.user)
    proposals = task.proposals.select_related('freelancer')
    return render(request, 'proposals/task_proposals.html',
                  {'task': task, 'proposals': proposals})

@login_required
def award_proposal(request, proposal_id):
    """Award a proposal to a freelancer (Client only)"""
    proposal = get_object_or_404(Proposal, id=proposal_id)
    task = proposal.task
    
    # Only task owner can award
    if task.client != request.user:
        messages.error(request, "You don't have permission to award this proposal.")
        return redirect('tasks:task_detail', task_id=task.id)
    
    # Check if task is still open
    if task.status != 'open':
        messages.error(request, "This task is no longer open for proposals.")
        return redirect('proposals:task_proposals', task_id=task.id)
    
    # Check if proposal is still pending
    if proposal.status != 'pending':
        messages.error(request, "This proposal has already been processed.")
        return redirect('proposals:task_proposals', task_id=task.id)
    
    # Award the proposal (atomic transaction)
    from django.db import transaction
    
    with transaction.atomic():
        # Update proposal status
        proposal.status = 'awarded'
        proposal.save()
        
        # Update task status
        task.status = 'in_progress'
        task.save()
        
        # Reject all other pending proposals for this task
        Proposal.objects.filter(task=task, status='pending').exclude(id=proposal.id).update(status='rejected')
    
    messages.success(request, f"Proposal awarded to {proposal.freelancer.get_full_name()}!")
    return redirect('proposals:task_proposals', task_id=task.id)

@login_required
def reject_proposal(request, proposal_id):
    """Reject a proposal (Client only)"""
    proposal = get_object_or_404(Proposal, id=proposal_id)
    task = proposal.task
    
    # Only task owner can reject
    if task.client != request.user:
        messages.error(request, "You don't have permission to reject this proposal.")
        return redirect('proposals:task_proposals', task_id=task.id)
    
    # Check if proposal is still pending
    if proposal.status != 'pending':
        messages.error(request, "This proposal has already been processed.")
        return redirect('proposals:task_proposals', task_id=task.id)
    
    # Reject the proposal
    proposal.status = 'rejected'
    proposal.save()
    
    messages.success(request, "Proposal rejected.")
    return redirect('proposals:task_proposals', task_id=task.id)
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
@login_required
def task_proposals(request, task_id):
    """View all proposals for a specific task (Client only)"""
    task = get_object_or_404(Task, id=task_id)
    
    # Only task owner can view proposals
    if task.client != request.user:
        messages.error(request, "You don't have permission to view these proposals.")
        return redirect('tasks:task_detail', task_id=task.id)
    
    # Get all proposals for this task, ordered by submission date
    proposals = Proposal.objects.filter(task=task).select_related('freelancer').order_by('-created_at')
    
    # Count proposals by status
    total_count = proposals.count()
    pending_count = proposals.filter(status='pending').count()
    awarded_count = proposals.filter(status='awarded').count()
    
    context = {
        'task': task,
        'proposals': proposals,
        'total_count': total_count,
        'pending_count': pending_count,
        'awarded_count': awarded_count,
    }
    
    return render(request, 'proposals/task_proposals.html', context)
@login_required
def award_proposal(request, proposal_id):
    """Award a proposal to a freelancer (Client only)"""
    proposal = get_object_or_404(Proposal, id=proposal_id)
    task = proposal.task
    
    # Only task owner can award
    if task.client != request.user:
        messages.error(request, "You don't have permission to award this proposal.")
        return redirect('tasks:task_detail', task_id=task.id)
    
    # Check if task is still open
    if task.status != 'open':
        messages.error(request, "This task is no longer open for proposals.")
        return redirect('proposals:task_proposals', task_id=task.id)
    
    # Check if proposal is still pending
    if proposal.status != 'pending':
        messages.error(request, "This proposal has already been processed.")
        return redirect('proposals:task_proposals', task_id=task.id)
    
    # Award the proposal (atomic transaction)
    with transaction.atomic():
        # Update proposal status
        proposal.status = 'awarded'
        proposal.save()
        
        # Update task status
        task.status = 'in_progress'
        task.save()
        
        # Reject all other pending proposals for this task
        Proposal.objects.filter(task=task, status='pending').exclude(id=proposal.id).update(status='rejected')
    
    messages.success(request, f"Proposal awarded to {proposal.freelancer.get_full_name()}!")
    return redirect('proposals:task_proposals', task_id=task.id)
@login_required
def reject_proposal(request, proposal_id):
    """Reject a proposal (Client only)"""
    proposal = get_object_or_404(Proposal, id=proposal_id)
    task = proposal.task
    
    # Only task owner can reject
    if task.client != request.user:
        messages.error(request, "You don't have permission to reject this proposal.")
        return redirect('tasks:task_detail', task_id=task.id)
    
    # Check if proposal is still pending
    if proposal.status != 'pending':
        messages.error(request, "This proposal has already been processed.")
        return redirect('proposals:task_proposals', task_id=task.id)
    
    # Reject the proposal
    proposal.status = 'rejected'
    proposal.save()
    
    messages.success(request, "Proposal rejected.")
    return redirect('proposals:task_proposals', task_id=task.id)
@login_required
def complete_task(request, proposal_id):
    """Mark task as completed and submit review (Client only)"""
    proposal = get_object_or_404(Proposal, id=proposal_id)
    task = proposal.task
    
    # Only task owner can complete
    if task.client != request.user:
        messages.error(request, "You don't have permission to complete this task.")
        return redirect('proposals:task_proposals', task_id=task.id)
    
    # Check if proposal is awarded
    if proposal.status != 'awarded':
        messages.error(request, "This proposal is not awarded.")
        return redirect('proposals:task_proposals', task_id=task.id)
    
    # Check if task is in progress
    if task.status != 'in_progress':
        messages.error(request, "This task is not in progress.")
        return redirect('proposals:task_proposals', task_id=task.id)
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        # Validate rating
        if not rating or not comment:
            messages.error(request, "Please provide both rating and comment.")
            return redirect('proposals:task_proposals', task_id=task.id)
        
        # Create review and complete task (atomic transaction)
        with transaction.atomic():
            # Create review
            Review.objects.create(
                task=task,
                proposal=proposal,
                reviewer=request.user,
                freelancer=proposal.freelancer,
                rating=int(rating),
                comment=comment
            )
            
            # Update task status
            task.status = 'completed'
            task.save()
        
        messages.success(request, f"Task marked as completed! Review submitted for {proposal.freelancer.get_full_name()}.")
        return redirect('tasks:client_dashboard')
    
    return redirect('proposals:task_proposals', task_id=task.id)