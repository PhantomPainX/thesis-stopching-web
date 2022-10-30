from django.contrib import admin
from .models import *

@admin.register(New)
class NewAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'created_at',
        'updated_at',
        'image',
        'category',
        'detection_accuracy',
        'ai_classification'
    )
    search_fields = ('title',)
    list_filter = ('category','ai_classification',)

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

@admin.register(NewSection)
class NewSectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'new', 'title', 'created_at', 'updated_at')
    search_fields = ('content',)

@admin.register(NewsImage)
class NewsImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'new', 'image', 'remote_image', 'note', 'created_at', 'updated_at')
    search_fields = ('note',)

@admin.register(UserExtra)
class UserExtraAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'g_prefered_categories')

    def g_prefered_categories(self, obj):
        return ",\n".join([p.category.name for p in UserCategory.objects.all()])

@admin.register(UserCategory)
class UserCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_extra', 'category', 'created_at')
