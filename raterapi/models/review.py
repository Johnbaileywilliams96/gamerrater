from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from .game import Game


class GameReview(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='game_reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='game_reviews')
    review_text = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)

    
    
