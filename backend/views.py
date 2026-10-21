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
from .pagination import CustomPagination
from .permissions import IsAuthorOrReadOnly, IsAuthorOrUser, IsSelfOrReadOnly
from django.db import transaction
from django.db.models import Count
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
from .tasks import send_user_notification


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().select_related("author")
    serializer_class = PostSerializers
    pagination_class = CustomPagination
    ordering_fields = ["posted_time", "likes_count"]
    search_fields = ["text", "author__username"]
    permission_classes = [IsAuthorOrUser]

    @action(detail=True, methods=["post"])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        liked_post, created = Like.objects.get_or_create(post=post, user=user)
        if not created:
            return Response(
                "You have already liked this post!", status=status.HTTP_400_BAD_REQUEST
            )
        else:
            return Response(
                "Like successfully added",
                status=status.HTTP_201_CREATED,
            )

    @action(detail=True, methods=["delete"])
    def unlike(self, request, pk=None):
        post = self.get_object()
        user = request.user
        like = get_object_or_404(Like, post=post, user=user)
        like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer):
        post = serializer.save(author=self.request.user)

        notification_text = (
            f"Your post '{post.text[:10]}...' has been successfully published!"
        )

        transaction.on_commit(
            lambda: send_user_notification.apply_async(
                args=[post.author.id, notification_text], countdown=10
            )
        )

    def get_queryset(self):
        if self.action == "like" or self.action == "unlike":
            return Post.objects.all()
        if not self.request.user.is_authenticated:
            return Post.objects.none()
        if self.action == "list":
            following_ids = Follow.objects.filter(
                follower=self.request.user
            ).values_list("following", flat=True)
            return Post.objects.filter(author__in=following_ids).annotate(
                likes_count=Count("like")
            )
        return Post.objects.all()


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomSerializers
    permission_classes = [IsSelfOrReadOnly]

    @action(detail=True, methods=["post"])
    def follow(self, request, pk=None):
        following = self.get_object()
        follower = request.user
        if Follow.objects.filter(
            follower=follower,
            following=following,
        ).exists():
            return Response(
                "You are already subscribed to this user!",
                status=status.HTTP_400_BAD_REQUEST,
            )
        if following == follower:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        Follow.objects.create(follower=follower, following=following)
        return Response("Successful", status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["delete"])
    def unfollow(self, request, pk=None):
        following = self.get_object()
        follower = request.user
        follow = get_object_or_404(
            Follow,
            following=following,
            follower=follower,
        )
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        return CustomUser.objects.annotate(
            followers_count=Count("followers"),
            following_count=Count("my_following"),
        )


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().select_related("user")
    serializer_class = CommentSerializers
    filterset_fields = ["post"]
    permission_classes = [IsAuthorOrUser]

    def get_queryset(self):
        post_pk = self.kwargs.get("post_pk")
        if post_pk:
            return Comment.objects.filter(post=post_pk)
        return Comment.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.all().select_related("author")
    serializer_class = StorySerializers
    permission_classes = [IsAuthorOrReadOnly]

    @action(detail=True, methods=["post"])
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
        return (
            Story.objects.filter(created_at__gte=delta)
            .select_related("author")
            .annotate(view_count=Count("storyview"))
        )


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializers

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)
