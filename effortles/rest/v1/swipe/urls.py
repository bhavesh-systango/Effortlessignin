from django.urls import path
from .views import MakeSwipeViewSet
from rest_framework.routers import DefaultRouter



router = DefaultRouter()
router.register(r'makeswipe', MakeSwipeViewSet, basename='makeswipe')
urlpatterns = router.urls
