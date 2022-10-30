from django.contrib.auth.models import User, Group
from .models import *
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):

    # extra = serializers.SerializerMethodField(read_only=True)
    # def get_extra(self, obj):
    #     return UserExtra.objects.filter(user=obj.id).values()

    user_extra = serializers.SerializerMethodField(read_only=True)
    def get_user_extra(self, obj):
        return UserExtra.objects.filter(user=obj.id).values()

    prefered_categories = serializers.SerializerMethodField(read_only=True)
    def get_prefered_categories(self, obj):
        return UserCategory.objects.filter(user_extra__user=obj.id).values()

    class Meta:
        model = User
        fields = ['id','url', 'username', 'email', 'first_name', 'last_name','groups', 'user_extra','prefered_categories',]

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