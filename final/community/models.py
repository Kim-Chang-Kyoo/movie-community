from django.db import models
from django.conf import settings

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from movies import models as a

class Review(models.Model):
    title = models.CharField(max_length=100)
    rank = models.IntegerField(choices=[(i, i) for i in range(0, 11)], blank=False)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_reviews')
    movie = models.ForeignKey(a.Movie, on_delete=models.CASCADE)


class Comment(models.Model):
    content = models.CharField(max_length=100)
    
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
