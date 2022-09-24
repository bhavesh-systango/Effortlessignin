from django.urls import path, include
 
urlpatterns = [
    path('feed/', include("rest.v1.feed.urls")),
    path('auth/', include("rest.v1.auth.urls")),
    path('swipe/', include("rest.v1.swipe.urls"))
]
