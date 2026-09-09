from django.db import models
import uuid

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('Parent', 'Parent'),
        ('Child', 'Child'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    pin_hash = models.CharField(max_length=128) # Hashed 4-digit PIN for profile switching
    total_points = models.IntegerField(default=0) # Cumulative monthly score
    level = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.name} ({self.role})"

class Chore(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    difficulty_points = models.IntegerField(default=10)

    def __str__(self):
        return self.title

class Assignment(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Submitted', 'Submitted For Review'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chore = models.ForeignKey(Chore, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    week_start_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    photo_url = models.URLField(blank=True, null=True) # Cloud storage link for photo proof

    def __str__(self):
        return f"{self.chore.title} -> {self.user.name} ({self.status})"
