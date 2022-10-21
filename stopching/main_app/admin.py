from django.contrib import admin
from .models import *

@admin.register(New)
class NewAdmin(admin.ModelAdmin):
    list_display = (
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
    )
    search_fields = ('title',)

@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name','description',)

@admin.register(AINewsClassification)
class AINewsClassificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'created_at', 'updated_at')
    search_fields = ('name','description',)

@admin.register(UserNewsClassification)
class UserNewsClassificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'created_at', 'updated_at')
    search_fields = ('name','description',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'new', 'user', 'content', 'in_response_to', 'created_at', 'updated_at')
    search_fields = ('content',)

@admin.register(NewsImage)
class NewsImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'new', 'image', 'created_at', 'updated_at')
    search_fields = ('content',)
