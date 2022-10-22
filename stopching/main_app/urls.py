from django.urls import path, include
from main_app.views import *

from rest_framework import routers
from main_app import api_views

router = routers.DefaultRouter()
router.register(r'users', api_views.UserViewSet)
router.register(r'news', api_views.NewViewSet, basename='news')
router.register(r'comments', api_views.CommentViewSet, basename='comments')
router.register(r'newsimages', api_views.NewsImageViewSet, basename='newsimages')
router.register(r'newscategories', api_views.NewsCategoryViewSet, basename='newscategories')

urlpatterns = [
    path('', home, name='home'),

    # API URLS
    path('api/v1/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]