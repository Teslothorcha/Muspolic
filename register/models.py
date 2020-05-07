from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_image = models.ImageField(default='profile_pics/default.png', upload_to='profile_pics')
    
    def __str__(self):
        return("{} Profile".format(self.user.username))