from .models import Proposal

def proposal_count(request):
    if request.user.is_authenticated:
        count = Proposal.objects.filter(
            freelancer=request.user
        ).count()
        pending_count = Proposal.objects.filter(
            freelancer=request.user,
            status='pending'
        ).count()
        return {
            'total_proposals_count': count,
            'pending_proposals_count': pending_count,
        }
    return {
        'total_proposals_count': 0,
        'pending_proposals_count': 0,
    }