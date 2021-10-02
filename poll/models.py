from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Poll(models.Model):
    question = models.CharField(max_length=200)
    no_of_option = models.IntegerField()
    time = models.IntegerField(help_text="duration of the poll in minutes")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question

    def get_option(self):
        return self.option_set.all()

class Option(models.Model):
    text = models.CharField(max_length=100)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.text