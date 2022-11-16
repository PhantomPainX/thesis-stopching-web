from django.urls import path, include
from main_app.views import *

from rest_framework import routers
from main_app import api_views
from main_app import new_api_views

router = routers.DefaultRouter()
router.register(r'users', api_views.UserViewSet)
# router.register(r'users-detail', api_views.UserDetail, basename='users-detail')
router.register(r'users-extra', api_views.UserExtraViewSet, basename='users-extra')
router.register(r'news', api_views.NewViewSet, basename='news')
router.register(r'comments', api_views.CommentViewSet, basename='comments')
router.register(r'news-images', api_views.NewsImageViewSet, basename='news-images')
router.register(r'news-categories', api_views.NewsCategoryViewSet, basename='news-categories')
router.register(r'user-categories', api_views.UserCategoriesViewSet, basename='user-categories')
router.register(r'ai-classifications', api_views.AINewsClassificationViewSet, basename='ai-classifications')
router.register(r'replies', api_views.CommentRepliesViewSet, basename='replies')

urlpatterns = [
    path('', home, name='home'),
    path('scrape/', scrape, name='scrape'),

    # API URLS
    path('api/v1/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/v1/user-categories/<int:pk>/', api_views.UserCategoriesDetailView.as_view()),
    path('api/v1/users-private-detail/<int:pk>/', api_views.UserPrivateDetail.as_view()),
    path('api/v1/users-public-detail/<int:pk>/', api_views.UserPublicDetail.as_view()),
    path('api/v1/signin/', api_views.signin),
    path('api/v1/signup/', api_views.signup),
    path('api/v1/predict/', api_views.predict_article),

    # API 2 URLS
    #path('api/v2/get-news/', new_api_views.get_last_news, name='get_last_news'),
]