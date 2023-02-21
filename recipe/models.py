from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):

    # Enforce unique mail address
    email = models.EmailField(unique=True)
    pass


# Recipe model
class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField(max_length=64)
    description = models.TextField(max_length=256)
    notes = models.TextField(max_length=256, blank=True) 
    directions = models.TextField(max_length=2048)
    ingredients = models.TextField(max_length=512)
    yummy = models.ManyToManyField(User, related_name="yummy", blank=True)
    time = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="images", blank=True)


# Profile model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    recipe = models.ManyToManyField(Recipe, related_name="recipe", blank=True)
    following = models.ManyToManyField(User, related_name="following", blank=True)
    followed_by = models.ManyToManyField(User, related_name="followed_by", blank=True)
    bio = models.TextField(max_length=128, blank=True)
    picture = models.ImageField(upload_to="images", blank=True) 


# List model
class List(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField(max_length=64)
    recipe = models.ManyToManyField(Recipe, related_name="list", blank=True) 


# Comment model
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    content = models.TextField(max_length=256)
    image = models.ImageField(upload_to="images", blank=True)
