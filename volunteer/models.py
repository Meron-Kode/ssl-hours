from django.db import models
from django.contrib.auth.models import User


class VolunteerLog(models.Model):
    # Links the log to a specific student user
    student = models.ForeignKey(User, on_delete=models.CASCADE)

    # Core SSL Form requirements
    organization_name = models.CharField(max_length=200)
    volunteer_date = models.DateField()
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2)

    # Addressing the "tedium" of manual verification
    supervisor_name = models.CharField(max_length=100)
    supervisor_email = models.EmailField()

    # Reflection as required by most schools
    reflection = models.TextField(help_text="What did you learn from this experience?")

    # Status tracking to replace the "waiting for counselor" anxiety
    STATUS_CHOICES = [
        ('P', 'Pending Approval'),
        ('A', 'Approved'),
        ('R', 'Rejected'),
    ]
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.organization_name} ({self.hours_worked} hrs)"
