from django.db import models
from django.conf import settings

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
    proposal = models.OneToOneField(
        Proposal,
        on_delete=models.CASCADE,
        related_name='review'
    )
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.proposal}"