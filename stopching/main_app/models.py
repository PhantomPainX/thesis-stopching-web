from datetime import datetime
from django.db import models
import datetime

from django.contrib.auth.models import User

class AINewsClassification(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class UserNewsClassification(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class NewsCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class New(models.Model):
    title = models.CharField(max_length=512)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='images/news/front/' + str(datetime.datetime.now().date()) + "/", blank=True, null=True)
    category = models.ForeignKey(NewsCategory, null=False, default=1, on_delete=models.SET_DEFAULT)
    detection_accuracy = models.FloatField()
    ai_classification = models.ForeignKey(AINewsClassification, null=True, blank=True, on_delete=models.SET_NULL)
    user_classification = models.ForeignKey(UserNewsClassification, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title

class Comment(models.Model):
    new = models.ForeignKey(New, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    in_response_to = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.new.title + " - " + self.user.username

class NewsImage(models.Model):
    new = models.ForeignKey(New, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/news/body/' + str(datetime.datetime.now().date()) + "/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.new.title