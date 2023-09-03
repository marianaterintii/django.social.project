

from django.db import models

from django.contrib.auth.models import User


# proxy EXTENDING model
class CustomUser(User):
    avatar = models.CharField(max_length=150,default="")   
    
    # FRIENDSHIP!!
    friends = models.ManyToManyField('self')
    

class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.CharField(max_length=200,default="")
 
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None)
    
####?

class Comment(models.Model):

    body = models.CharField(max_length=200,default="")
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.TextField(max_length=80)
    

  