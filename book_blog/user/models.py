from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    class Meta:
        ordering = ["-post_number", "-rate_number", "-user__date_joined"]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', default='default_avatar.png')
    description = models.CharField(max_length=100, default="")
    post_number = models.IntegerField(default=0)
    rate_number = models.FloatField(default=0.0)
    rate_changed = models.BooleanField(default=False)
    def __str__(self):
        return self.user.username