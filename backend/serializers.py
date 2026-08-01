from .models import (
    CustomUser,
    Like,
    Post,
    Follow,
    Comment,
    Story,
    Favorite,
)
from rest_framework import serializers


class CustomSerializers(serializers.ModelSerializer):
    followers_count = serializers.IntegerField(read_only=True)
    following_count = serializers.IntegerField(read_only=True)

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
            'followers_count',
            'following_count',
        ]


class PostSerializers(serializers.ModelSerializer):
    author = CustomSerializers(read_only=True)
    author_id = serializers.IntegerField(write_only=True, required=False)
    likes_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'author',
            'author_id',
            'text',
            'image',
            'posted_time',
            'likes_count',
        ]


class LikeSerializers(serializers.ModelSerializer):
    user = serializers.IntegerField(read_only=True, source='user_id')

    class Meta:
        model = Like
        fields = [
            'id',
            'post',
            'user',
            'created_at',
        ]


class FollowSerializers(serializers.ModelSerializer):
    follower = serializers.IntegerField(read_only=True, source='follower_id')

    class Meta:
        model = Follow
        fields = [
            'id',
            'follower',
            'following',
        ]


class CommentSerializers(serializers.ModelSerializer):
    user = serializers.IntegerField(read_only=True, source='user_id')

    class Meta:
        model = Comment
        fields = [
            'id',
            'user',
            'post',
            'text',
            'created_at',
        ]


class StorySerializers(serializers.ModelSerializer):
    author = CustomSerializers(read_only=True)
    author_id = serializers.IntegerField(write_only=True, required=False)
    view_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Story
        fields = [
            'id',
            'author',
            'text',
            'image',
            'author_id',
            'created_at',
            'view_count'
        ]


class FavoriteSerializers(serializers.ModelSerializer):
    post = PostSerializers(read_only=True)
    post_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Favorite
        fields = [
            'id',
            'post',
            'post_id',
            'added_at',
        ]
