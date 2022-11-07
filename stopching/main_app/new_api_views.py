from unittest import result
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.authentication import TokenAuthentication
from rest_framework import permissions, viewsets
from rest_framework.views import APIView



@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes((permissions.DjangoModelPermissionsOrAnonReadOnly,))
def get_last_news2(request):
    #add pagination
    news = New.objects.all().order_by('-created_at')
    paginator = LimitOffsetPagination()
    result_page = paginator.paginate_queryset(news, request)

    #add rest framework pagination
    serializer = NewSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

