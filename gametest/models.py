from django.db import models

class Message(models.Model):
    sender = models.TextField()
    message = models.TextField()
    

# Create your models here.
