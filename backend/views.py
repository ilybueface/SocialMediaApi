from .models import (
    CustomUser,
    Like,
    Post,
    Follow,
    Comment,
)
from .serializers import (
    CustomSerializers,
    LikeSerializers,
    PostSerializers,
    FollowSerializers,
    CommentSerializers,
)
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializers

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        if Like.objects.filter(post=post, user=user).exists():
            return Response('Вы уже лайкнули этот пост', status=status.HTTP_400_BAD_REQUEST)
        Like.objects.create(post=post, user=user)
        return Response('Лайк успешно поставлен', status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['delete'])
    def unlike(self, request, pk=None):
        post = self.get_object()
        user = request.user
        like = get_object_or_404(Like, post=post, user=user)
        like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomSerializers

    @action(detail=True, methods=['post'])
    def follow(self, request, pk=None):
        following = self.get_object()
        follower = request.user
        if Follow.objects.filter(follower=follower, following=following).exists():
            return Response('Вы уже подписаны на данного пользователя', status=status.HTTP_400_BAD_REQUEST)
        if following == follower:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        Follow.objects.create(follower=follower, following=following)
        return Response('Успешно', status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['delete'])
    def unfollow(self, request, pk=None):
        following = self.get_object()
        follower = request.user
        follow = get_object_or_404(Follow, following=following, follower=follower)
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializers

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
