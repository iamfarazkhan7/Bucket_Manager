# File: buckets/models.py
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Bucket(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buckets')

    class Meta:
        unique_together = ['name', 'owner']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.owner.username})"

    def get_absolute_url(self):
        return reverse('buckets:detail', kwargs={'pk': self.pk})