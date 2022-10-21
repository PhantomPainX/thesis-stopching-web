from django.contrib.auth.models import User
from .models import *
from rest_framework import viewsets, generics, permissions, filters, status
from .serializers import *
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class NewViewSet(viewsets.ModelViewSet):
    serializer_class = NewSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['category', 'ai_classification', 'user_classification']
    search_fields = ['title']
    ordering_fields = ['created_at', 'updated_at']
    queryset = New.objects.all()

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    # filterset_fields = ['estreno', 'idioma', 'generos', 'tipo', 'estado']
    search_fields = ['content']
    ordering_fields = ['created_at', 'updated_at']
    queryset = Comment.objects.all()