from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from .game import Game

class GameRating(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='game_ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='game_ratings')
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Rating from 1 to 10"
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


