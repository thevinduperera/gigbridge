from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()
class Proposal(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('awarded', 'Awarded'),
        ('rejected', 'Rejected'),
    ]
    task = models.ForeignKey(
        'tasks.Task',
        on_delete=models.CASCADE,
        related_name='proposals'
    )
    freelancer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='submitted_proposals'
    )
    cover_letter = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    estimated_days = models.PositiveIntegerField()
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )
    reject_reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Proposal by {self.freelancer} for {self.task}"


class Review(models.Model):
    """Review left by client for freelancer after task completion"""
    task = models.OneToOneField('tasks.Task', on_delete=models.CASCADE, related_name='review')
    proposal = models.OneToOneField(Proposal, on_delete=models.CASCADE, related_name='review')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_given')
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_received')
    rating = models.IntegerField(
        choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')],
        help_text='Rating from 1 to 5 stars'
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Review for {self.freelancer.username} - {self.rating} stars"