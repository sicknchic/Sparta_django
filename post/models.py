from django.db import models
from django.conf import settings


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Post(TimeStampModel):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(
        to=settings.AUTH_USER_MODEL, related_name="like_posts"
    )

    def __str__(self):
        return self.title


class Comment(TimeStampModel):
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name="comments")
    message = models.CharField(max_length=140)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.post.title}의 댓글"
