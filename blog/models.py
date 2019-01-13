from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

#Post model
class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(unique_for_date="publish", max_length=250)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    likes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title
