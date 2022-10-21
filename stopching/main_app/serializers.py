from django.contrib.auth.models import User, Group
from .models import *
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id','url', 'username', 'email', 'groups']

class NewSerializer(serializers.ModelSerializer):

    category = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='name'
    )

    ai_classification = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='name'
    )

    user_classification = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = New
        fields = [
            'id',
            'title',
            'content',
            'created_at',
            'updated_at',
            'image',
            'category',
            'detection_accuracy',
            'ai_classification',
            'user_classification'
        ]

class CommentSerializer(serializers.ModelSerializer):
    new = NewSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Comment
        fields = [
            'id',
            'new',
            'user',
            'content',
            'in_response_to',
            'created_at',
            'updated_at'
        ]