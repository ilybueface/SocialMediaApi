from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    bio = models.TextField(blank=True)
    avatar = models.ImageField(null=True, blank=True, upload_to='avatars/')
    birth_date = models.DateField(null=True, blank=True)


class Post(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='posts/')
    posted_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['author', 'posted_time']),
        ]


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        unique_together = ('post', 'user')


class Follow(models.Model):
    follower = models.ForeignKey(CustomUser, related_name='my_following', on_delete=models.CASCADE)
    following = models.ForeignKey(CustomUser, related_name='followers', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['follower', 'following'],
                name='unique_follow'
                                    )
        ]


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Story(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    image = models.ImageField(blank=True, null=True, upload_to='story/')
    created_at = models.DateTimeField(auto_now_add=True)


class StoryView(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'story')


class Favorite(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')
