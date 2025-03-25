from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Game(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    designer = models.CharField(max_length=255)
    year_released = models.IntegerField()
    min_players = models.PositiveIntegerField()
    max_players = models.PositiveIntegerField()
    estimated_play_time = models.PositiveIntegerField(help_text="Estimated play time in minutes")
    age_recommendation = models.PositiveIntegerField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_games')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    