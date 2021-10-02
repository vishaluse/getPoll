from django.db import models
from django.db.models.fields.related import OneToOneField
from django.contrib.auth.models import User
from poll.models import Poll

# Create your models here.

class Result(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.pk