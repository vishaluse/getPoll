from django.db import models
from django.contrib.auth.models import User


# Create your models here.





class Poll(models.Model):
    question = models.CharField(max_length=200)
    is_eligible = models.BooleanField(default=False)
    time = models.IntegerField(help_text="duration of the poll in minutes")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

   

    def __str__(self):
        return self.question

    def get_option(self):
        return self.option_set.all()
    
    def get_image(self):
        return self.imageoption_set.all()



class PollHistory(models.Model) :
    is_voted = models.BooleanField(default=False)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.poll.question
    




class Option(models.Model):
    text = models.CharField(max_length=100)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.text

class ImageOption(models.Model):
    image = models.ImageField(null=True, blank=True, upload_to="images/%Y/%m/%d/")
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)

    def __str__(self):
        return str(self.poll.user)