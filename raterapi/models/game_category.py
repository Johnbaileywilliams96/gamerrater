from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from .game import Game
from .category import Category


# from django.db import models
# from django.contrib.auth.models import User


class GameCategory(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='categories')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='games')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_categories')
    created_at = models.DateTimeField(default=timezone.now)