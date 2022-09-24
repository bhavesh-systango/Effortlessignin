from authentication.models import User
from rest_framework.validators import UniqueTogetherValidator
from rest_framework import serializers
from feed.models import Post
from feed.models import Like, Comment


class PostSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        many=False, 
        read_only=False,
        queryset=User.objects.all(),
    )

    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Post
        fields = [
            'user',
            'body',
            'created_at',
            'updated_at',
        ]


class CommentSerializer(serializers.ModelSerializer):

    post = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=False, 
        queryset=Post.objects.all(),
        required=False,
    )

    user = serializers.PrimaryKeyRelatedField(
        many=False, 
        read_only=False,
        queryset=User.objects.all(),
    )

    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id',
            'post',
            'user',
            'comment',
            'created_at',
            'updated_at',
        ]


class LikeSerializer(serializers.ModelSerializer):

    post = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=False, 
        queryset=Post.objects.all(),
        required=False,
    )

    user = serializers.PrimaryKeyRelatedField(
        many=False, 
        read_only=False,
        queryset=User.objects.all(),
        required=False,
    )
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Like
        fields = [
            'id',
            'post',
            'comment',
            'user',
            'like_type',
            'created_at',
            'updated_at',
        ]

        def get_validation_exclusions(self):
            exclusions = super(LikeSerializer, self).get_validation_exclusions()
            return exclusions + ['post', 'comment']

        validators = [
            UniqueTogetherValidator(
                queryset=Like.objects.all(),
                fields=['post', 'user']
            )
        ]
