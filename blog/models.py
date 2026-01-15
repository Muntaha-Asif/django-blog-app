from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.db.models import Count


class Profile(models.Model):
    """Extended user profile"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png', blank=True)
    website = models.URLField(max_length=200, blank=True)
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'


class Category(models.Model):
    """Blog post categories"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=300, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category-posts', kwargs={'slug': self.slug})


class Post(models.Model):
    """Blog Post Model"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='published')
    views = models.IntegerField(default=0)

    class Meta:
        ordering = ['-date_posted']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def total_likes(self):
        return self.likes.count()

    def total_comments(self):
        return self.comments.count()

    def reading_time(self):
        """Calculate reading time in minutes"""
        word_count = len(self.content.split())
        minutes = word_count // 200  # Average reading speed: 200 words/min
        return max(1, minutes)


class Like(models.Model):
    """Post likes"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f'{self.user.username} likes {self.post.title}'


class Comment(models.Model):
    """Post comments"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    class Meta:
        ordering = ['-date_posted']

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'