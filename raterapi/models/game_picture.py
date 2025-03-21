# from django.db import models
# from django.contrib.auth.models import User
# from django.utils import timezone


# class GamePicture(models.Model):
#     game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='pictures')
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_pictures')
#     image_url = models.URLField()
#     caption = models.TextField(blank=True, null=True)
#     created_at = models.DateTimeField(default=timezone.now)

