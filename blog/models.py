from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager

#Published Post Manager for Post model
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')

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
    tags = TaggableManager()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    like_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    objects = models.Manager() # the default manager
    published = PublishedManager() # our custom manager

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                        args=[ self.publish.day, self.publish.month, self.publish.year, self.slug])


#Comment Model
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField( max_length=80, blank=True, default="Anonymous")
    email = models.EmailField(blank=True, default="user@email.com")
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True) #to delete any comment by admin

    class Meta:
        ordering = ('created', )

    def __str__(self):
        return "Comment by {} on {}".format(self.name, self.post)

#Subscribe model
class Subscribe(models.Model):
    name = models.CharField(max_length=80)
    email = models.EmailField(unique=True)
    request_on = models.DateTimeField(auto_now_add=True)
    subscribed_on = models.DateTimeField(auto_now=True)
    confirm_token = models.CharField(max_length=100)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return "{} subscribed on {}".format(self.name, self.subscribed_on)