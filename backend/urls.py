from rest_framework.routers import DefaultRouter
from .views import (
    PostViewSet,
    UserViewSet,
    CommentViewSet,
)


router = DefaultRouter()
router.register(r'post', PostViewSet, basename='Post')
router.register(r'user', UserViewSet, basename='User')
router.register(r'comment', CommentViewSet, basename='Comment')



urlpatterns = router.urls