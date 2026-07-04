from .models import (
    CustomUser,
    Like,
    Post,
    Follow,
    Comment,
)
from rest_framework import serializers


class CustomSerializers(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'bio',
            'avatar',
            'birth_date',
        ]


class PostSerializers(serializers.ModelSerializer):
    author = CustomSerializers(read_only=True)
    author_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Post
        fields = [
            'id',
            'author',
            'author_id',
            'text',
            'image',
            'posted_time',
        ]


class LikeSerializers(serializers.ModelSerializer):
    user = serializers.IntegerField(read_only=True)

    class Meta:
        model = Like
        fields = [
            'id',
            'post',
            'user',
            'created_at',
        ]


class FollowSerializers(serializers.ModelSerializer):
    follower = serializers.IntegerField(read_only=True)

    class Meta:
        model = Follow
        fields = [
            'id',
            'follower',
            'following',
        ]


class CommentSerializers(serializers.ModelSerializer):
    user = serializers.IntegerField(read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id',
            'user',
            'post',
            'text',
            'created_at',
        ]
