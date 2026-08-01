from .models import (
    CustomUser,
    Like,
    Post,
    Follow,
    Comment,
    Story,
    StoryView,
    Favorite,
)
from .serializers import (
    CustomSerializers,
    PostSerializers,
    CommentSerializers,
    StorySerializers,
    FavoriteSerializers,
)
from rest_framework.filters import SearchFilter
from .pagination import CustomPagination
from .permissions import (
    IsAuthorOrReadOnly,
    IsAuthorOrUser,
    IsSelfOrReadOnly
)
from django.db.models import Count
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializers
    pagination_class = CustomPagination
    ordering_fields = ['posted_time', 'likes_count']
    search_fields = ['text', 'author__username']
    permission_classes = [IsAuthorOrReadOnly]

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
        following_ids = (Follow.objects.filter(follower=self.request.user)
                        .values_list('following', flat=True))
        followed_users_posts = (Post.objects.filter(author__in=following_ids)
                                .annotate(likes_count=Count('like')))
        return followed_users_posts


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomSerializers
    permission_classes = [IsSelfOrReadOnly]

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

    def get_queryset(self):
        return CustomUser.objects.annotate(followers_count=Count('followers'),
                                    following_count=Count('my_following')
                                    )



class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializers
    filterset_fields = ['post']
    permission_classes = [IsAuthorOrUser]

    def get_queryset(self):
        post_pk = self.kwargs.get('post_pk')
        if post_pk:
            return Comment.objects.filter(post=post_pk)
        return Comment.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.all()
    serializer_class = StorySerializers
    permission_classes = [IsAuthorOrReadOnly]

    @action(detail=True, methods=['post'])
    def story_view(self, request, pk=None):
        story = self.get_object()
        user = request.user
        if StoryView.objects.filter(story=story, user=user).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        StoryView.objects.create(story=story, user=user)
        return Response(status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        delta = timezone.now() - timedelta(hours=24)
        return (Story.objects.filter(created_at__gte=delta)
                .annotate(view_count=Count('storyview')))


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializers

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)