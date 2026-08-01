from rest_framework_nested import routers
from .views import (
    PostViewSet,
    UserViewSet,
    CommentViewSet,
    StoryViewSet,
    FavoriteViewSet
)


router = routers.DefaultRouter()
router.register(r'post', PostViewSet, basename='Post')
router.register(r'user', UserViewSet, basename='User')
router.register(r'comment', CommentViewSet, basename='Comment')
router.register(r'story', StoryViewSet, basename='Story')
router.register(r'favorite', FavoriteViewSet, basename='Favorite')
comment_router = routers.NestedDefaultRouter(router, r'post', lookup='post')
comment_router.register(r'comments', CommentViewSet, basename='post-comments')

urlpatterns = router.urls + comment_router.urls