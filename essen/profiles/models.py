from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Member(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    class_year = models.IntegerField(null=True)
    major = models.CharField(max_length=20, null=True)
    bio = models.TextField(null=True)
    image = models.ImageField(upload_to="images/", null=True)

    def __str__(self):
        return self.user.get_full_name()
