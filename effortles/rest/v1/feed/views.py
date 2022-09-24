from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import PostSerializer, LikeSerializer, CommentSerializer
from feed.models import Post, Like, Comment

User = get_user_model()


@api_view(['GET'])
def Test(request):
    return Response({'msg': "test working here"})


class PostViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user'] 

    def get_queryset(self):
        if self.request.method == "GET":
            queryset = Post.objects.all()

        else:
            queryset = Post.objects.filter(user=self.request.user.id).all()


        create_at = self.request.query_params.get('create_at')
        update_at = self.request.query_params.get('update_at')
        
        if create_at is not None:
            entered_date = create_at.split("-")
            entered_year = int(entered_date[0])
            entered_month = int(entered_date[1])
            entered_day = int(entered_date[2])
            queryset = queryset.filter(created_at__date=f"{entered_year}-{entered_month}-{entered_day}")

        if update_at is not None:
            entered_date = update_at.split("-")
            entered_year = int(entered_date[0])
            entered_month = int(entered_date[1])
            entered_day = int(entered_date[2])
            queryset = queryset.filter(updated_at__date=f"{entered_year}-{entered_month}-{entered_day}")

        return queryset
        
    def create(self, request, *args, **kwargs):
        '''
            overrided created method for following:

            - passing the user id to the serializer
        '''

        data_dict = request.data.copy()
        data_dict.update({'user':request.user.id})
        serializer = self.get_serializer(data=data_dict)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CommentViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['post', 'user']


    def get_queryset(self):
        '''
            overrided get_queryset method for following:

            - to check what request method is being used and 
              based on that, assigned the queryset objet to 
              queryset variable.
            
            - apply filter on date (created_at and updated_at)  
        '''

        if self.request.method == "GET":
            queryset = Comment.objects.all()

        else:
            queryset = Comment.objects.filter(user=self.request.user.id).all()

        create_at = self.request.query_params.get('create_at')
        update_at = self.request.query_params.get('update_at')
        
        if create_at is not None:
            entered_date = create_at.split("-")
            entered_year = int(entered_date[0])
            entered_month = int(entered_date[1])
            entered_day = int(entered_date[2])
            queryset = queryset.filter(created_at__date=f"{entered_year}-{entered_month}-{entered_day}")

        if update_at is not None:
            entered_date = update_at.split("-")
            entered_year = int(entered_date[0])
            entered_month = int(entered_date[1])
            entered_day = int(entered_date[2])
            queryset = queryset.filter(updated_at__date=f"{entered_year}-{entered_month}-{entered_day}")


        return queryset

    def create(self, request, *args, **kwargs):
        '''
            overrided created method for following:

            - passing the user id to the serializer
        '''
        user_id = request.user.id
        data_dict = request.data.copy()
        data_dict.update({'user': user_id})
        serializer = self.get_serializer(data=data_dict)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class LikeViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'delete']
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['post', 'comment', 'user', 'like_type'] 

    def get_queryset(self):
        if self.request.method == "GET":
            queryset = Like.objects.all()

        else:
            queryset = Like.objects.filter(user=self.request.user.id).all()

        create_at = self.request.query_params.get('create_at')
        update_at = self.request.query_params.get('update_at')
        
        if create_at is not None:
            entered_date = create_at.split("-")
            entered_year = int(entered_date[0])
            entered_month = int(entered_date[1])
            entered_day = int(entered_date[2])
            queryset = queryset.filter(created_at__date=f"{entered_year}-{entered_month}-{entered_day}")

        if update_at is not None:
            entered_date = update_at.split("-")
            entered_year = int(entered_date[0])
            entered_month = int(entered_date[1])
            entered_day = int(entered_date[2])
            queryset = queryset.filter(updated_at__date=f"{entered_year}-{entered_month}-{entered_day}")


        return queryset

    def create(self, request, *args, **kwargs):
        '''
            overrided created method for following:

            - passing the user id to the serializer
        '''

        user_id = request.user.id
        data_dict = request.data.copy()
        data_dict.update({'user': user_id})
        serializer = self.get_serializer(data=data_dict)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
