from django.contrib.auth.models import User, Group
from .models import *
from rest_framework import serializers
from rest_framework.authtoken.models import Token

class UserSerializer(serializers.ModelSerializer):

    user_extra = serializers.SerializerMethodField(read_only=True)
    def get_user_extra(self, obj):
        return UserExtra.objects.filter(user=obj.id).values()

    token = serializers.SerializerMethodField(read_only=True)
    def get_token(self, obj):
        token, created = Token.objects.get_or_create(user=obj)
        return token.key
        

    prefered_categories = serializers.SerializerMethodField(read_only=True)
    def get_prefered_categories(self, obj):
        return UserCategory.objects.filter(user_extra__user=obj.id).values()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'token',
            'first_name',
            'last_name',
            'is_staff',
            'is_superuser',
            'is_active',
            'date_joined',
            'last_login',
            'groups',
            'user_extra',
            'prefered_categories'
        ]

class UserExtraSerializer(serializers.ModelSerializer):

    prefered_categories = serializers.SerializerMethodField(read_only=True)
    def get_prefered_categories(self, obj):
        return UserCategory.objects.filter(user_extra=obj.id).values()

    class Meta:
        model = UserExtra
        fields = ['id', 'user', 'image', 'prefered_categories']

class UserPublicSerializer(serializers.ModelSerializer):

    user_extra = serializers.SerializerMethodField(read_only=True)
    def get_user_extra(self, obj):
        return UserExtra.objects.filter(user=obj.id).values('image')

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name','user_extra',]

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

    user_classifications = serializers.SerializerMethodField(read_only=True)
    def get_user_classifications(self, obj):
        return UsersClassification.objects.filter(new=obj.id).values()

    sections = serializers.SerializerMethodField(read_only=True)
    def get_sections(self, obj):
        return NewSection.objects.filter(new=obj.id).values()

    images = serializers.SerializerMethodField(read_only=True)
    def get_images(self, obj):
        #return parsed data
        return NewsImage.objects.filter(new=obj.id).values()

    class Meta:
        model = New
        fields = [
            'id',
            'title',
            'author',
            'new_date',
            'created_at',
            'updated_at',
            'image',
            'remote_image',
            'category',
            'detection_accuracy',
            'ai_classification',
            'user_classifications',
            'sections',
            'images',
        ]

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    replies = serializers.SerializerMethodField(read_only=True)
    def get_replies(self, obj):
        return CommentReplies.objects.filter(comment=obj.id).count()
    
    class Meta:
        model = Comment
        fields = [
            'id',
            'new',
            'user',
            'content',
            'replies',
            'created_at',
            'updated_at'
        ]

    def create(self, validated_data):
        new = validated_data['new']
        user = self.context['request'].user

        comment = Comment.objects.filter(
            new=new,
            user=user,
            content=validated_data['content']
        )
        if comment.exists():
            raise serializers.ValidationError({'error': 'Ya has comentado esto'})
        else:
            # clean_comment = palabrota.censor(validated_data['comment'])

            comment = Comment.objects.create(
                new=new,
                user=user,
                content=validated_data['content']
            )
            return comment

class CommentRepliesSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = CommentReplies
        fields = [
            'id',
            'comment',
            'user',
            'content',
            'created_at',
            'updated_at'
        ]

    def create(self, validated_data):
        comment = validated_data['comment']
        user = self.context['request'].user

        reply = CommentReplies.objects.filter(
            comment=comment,
            user=user,
            content=validated_data['content']
        )
        if reply.exists():
            raise serializers.ValidationError({'error': 'Ya has replicado esto'})
        else:
            # clean_comment = palabrota.censor(validated_data['comment'])

            reply = CommentReplies.objects.create(
                comment=comment,
                user=user,
                content=validated_data['content']
            )
            return reply

class NewsImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = NewsImage
        fields = [
            'id',
            'new',
            'image',
            'remote_image',
            'created_at',
            'updated_at'
        ]

class NewsCategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = NewsCategory
        fields = [
            'id',
            'name',
            'description'
        ]

class UserCategorySerializer(serializers.ModelSerializer):

    category = NewsCategorySerializer(read_only=False)

    class Meta:
        model = UserCategory
        fields = [
            'id',
            'user_extra',
            'category',
            'created_at'
        ]

class AINewsClassificationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AINewsClassification
        fields = [
            'id',
            'name',
            'description',
            'created_at',
            'updated_at'
        ]