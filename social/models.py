from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    display_name = models.CharField(max_length=200, default=None)
    image = models.ImageField(default='default.jpg', upload_to='images/%Y/%m/%d/')
    follow = models.ManyToManyField("self", blank=True)
    bio = models.CharField(max_length=255, blank=True)
    
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='comments')

    class Meta:
        ordering = ['date']
    
    def publish(self):
        self.date = timezone.now()
        self.save()
    
    def __str__(self):
        return 'Comment {} by {}'.format(self.text, self.author)
