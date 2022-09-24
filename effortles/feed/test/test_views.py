from django.test import Client, TestCase
from .test_setup import TestSetUp
from rest_framework import status
from rest_framework.test import force_authenticate
from feed.models import Post
from rest.v1.feed.serializers import PostSerializer

client = Client()

class TestAuthenticationApi(TestSetUp):

    def test_user_can_authenticate(self):
        """
        Ensure we can create a new account object.
        """
        data = {
            'email':'amverma@isystango.com',
            'password':'admin12345'
        }
        response = self.client.post(self.api_authenticate, data,format='json')
        # response = self.client.login(username='amverma@isystango.com', password='admin12345')
        print("****************************")
        print(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)



class TestPostApi(TestCase):

    def test_post_get(self):
        """
        -
        """
        # force_authenticate(self.request, user=None, token=None)
        response = client.get('api/v1/feed/post/')
        puppies = Post.objects.all()
        serializer = PostSerializer(puppies, many=True)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
