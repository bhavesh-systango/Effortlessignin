from django.db import models
from django.db.models import Q
from django.contrib.auth import get_user_model


User = get_user_model()


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    body = models.TextField(default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=1024, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Like(models.Model):

    LIKE_TYPE = [
        ("post","post"),
        ("comment","comment")
    ]

    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    like_type = models.CharField(choices=LIKE_TYPE, max_length=16, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [
            ['post','user'],
            ['comment','user']
        ]

        constraints = [
            models.CheckConstraint(
                check= Q( (Q(post=None) & ~Q(comment=None)) | (~Q(post=None) & Q(comment=None)) ),
                name="post_and_comment_field_mutually_exclusive"
            ),
        ]
