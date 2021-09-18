from django.db import models
from django.contrib.auth.models import User
class Administrator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)


    def __str__(self):
        return self.user.username



