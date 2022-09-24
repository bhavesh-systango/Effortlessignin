import this
from rest_framework.test import APITestCase, URLPatternsTestCase
from django.urls import include, path, reverse
# from model_bakery import baker


class TestSetUp(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('api/', include('rest.urls')),
    ]

    def setUp(self):
        self.api_authenticate = reverse('token_obtain_pair')
        self.api_post = reverse('api/v1/feed/post/')
        self.api_like = reverse('like')
        self.api_comment = reverse('comment')
        return super().setUp()

    def tearDown(self):
        return super().tearDown()


