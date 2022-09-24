from django.urls import path
from .views import Test, PostViewSet, LikeViewSet, CommentViewSet
from rest_framework.routers import DefaultRouter



router = DefaultRouter()
router.register(r'post', PostViewSet, basename='post')
router.register(r'like', LikeViewSet, basename='like')
router.register(r'comment', CommentViewSet, basename='comment')
urlpatterns = router.urls
