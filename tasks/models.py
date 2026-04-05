from django.db import models
from django.contrib.auth import get_user_model

# Using get_user_model() here instead of importing User directly
User = get_user_model()


class Category(models.Model):
    # Categories like "Web Development" or "Graphic Design"
    # are created by the admin and used to organise tasks
    # on the browse page.

    name = models.CharField(max_length=100)
    icon = models.CharField(
        max_length=50,
        help_text="Bootstrap icon class e.g. 'bi-code-slash'"
    )
    slug = models.SlugField(
        unique=True,
        # Used in URLs e.g. /tasks/category/web-development/
        # Auto-filled in the admin panel based on the name
        help_text="URL-friendly name e.g. 'web-development'"
    )

    class Meta:
        verbose_name_plural = "Categories"  # without this Django shows "Categorys" in admin
        ordering = ['name']

    def __str__(self):
        return self.name


class Skill(models.Model):
    # Skills like "Python", "React", "Photoshop" etc.
    # Used in two places - tasks list what skills they need,
    # and freelancer profiles list what skills they have.
    # We define Skill here in the tasks app to avoid circular
    # imports since accounts will import Skill from here.

    name = models.CharField(
        max_length=100,
        unique=True  # prevents duplicates like two entries for "Python"
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Task(models.Model):
    # A task is a job posted by a client.
    # The typical flow is: open → in_progress (once awarded) → completed (once client confirms)
    # A client can also cancel a task if no one has been awarded yet.

    STATUS_OPEN        = 'open'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_COMPLETED   = 'completed'
    STATUS_CANCELLED   = 'cancelled'

    STATUS_CHOICES = [
        (STATUS_OPEN,        'Open'),
        (STATUS_IN_PROGRESS, 'In Progress'),
        (STATUS_COMPLETED,   'Completed'),
        (STATUS_CANCELLED,   'Cancelled'),
    ]

    
    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posted_tasks'  
    )
    title = models.CharField(max_length=200)
    description = models.TextField()

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,  # keep the task even if the category gets deleted
        null=True,
        related_name='tasks'
    )
    skills_required = models.ManyToManyField(
        Skill,
        blank=True,  # not every task needs specific skills
        related_name='tasks'
    )

    # we use min and max to give clients flexibility in what they offer
    budget_min = models.DecimalField(max_digits=10, decimal_places=2)
    budget_max = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_OPEN  # every new task starts as open
    )
    deadline   = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)  # set once when created
    updated_at = models.DateTimeField(auto_now=True)      # updates on every save

    class Meta:
        ordering = ['-created_at']  # newest tasks show up first

    def __str__(self):
        return f"{self.title} [{self.get_status_display()}]"

    def is_open(self):
        # used in templates to show/hide the apply button
        return self.status == self.STATUS_OPEN

    def is_in_progress(self):
        return self.status == self.STATUS_IN_PROGRESS

    def is_completed(self):
        return self.status == self.STATUS_COMPLETED

    def proposal_count(self):
        # relies on the related_name='proposals' set in the Proposal model
        # in the proposals app - so this won't work its setup
        return self.proposals.count()

    def budget_display(self):
        return f"${self.budget_min:,.0f} - ${self.budget_max:,.0f}"
    