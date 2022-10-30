from django.contrib.auth.models import User
from .models import *
from rest_framework import viewsets, generics, permissions, filters, status
from .serializers import *
from rest_framework.response import Response
from django.contrib.auth import login, authenticate

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt

from main_app.scheduler.AI.ai_detection import AIDetection

# USER API VIEWS

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class UserPrivateDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        user = request.user
        if user.is_staff:
            if User.objects.filter(id=pk).exists():
                serializer = UserSerializer(User.objects.get(id=pk), many=False, context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if user.id != pk:
                return Response({"error": "You can only see your own user"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer = UserSerializer(User.objects.get(id=pk), many=False, context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, *args, **kwargs):
        user = request.user

        if not user.is_staff:
            if user.id != pk:
                return Response({"error": "You can only edit your own user"}, status=status.HTTP_400_BAD_REQUEST)

        username = user.username
        #email = user.email
        first_name = user.first_name
        last_name = user.last_name
        try:
            username = self.request.data['username']
            if User.objects.filter(username=username).exclude(id=request.user.id).exists():
                return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)
            user.username = username
        except:
            pass
        try:
            first_name = self.request.data['first_name']
            user.first_name = first_name
        except:
            pass
        try:
            last_name = self.request.data['last_name']
            user.last_name = last_name
        except:
            pass

        user.save()
        user_object = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user_object, many=False, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, *args, **kwargs):
        user = request.user
        if user.is_staff:
            if User.objects.filter(id=pk).exists():
                user = User.objects.get(id=pk)
                user.delete()
                return Response({"message": "User deleted"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if user.id != pk:
                return Response({"error": "You can only delete your own user"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                if User.objects.filter(id=pk).exists():
                    user = User.objects.get(id=pk)
                    user.delete()
                    return Response({"message": "User deleted"}, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST)

class UserPublicDetail(generics.RetrieveAPIView):
    serializer_class = UserPublicSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        if User.objects.filter(id=pk).exists():
            serializer = UserPublicSerializer(User.objects.get(id=pk), many=False, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST)

class UserExtraViewSet(viewsets.ModelViewSet):
    queryset = UserExtra.objects.all()
    serializer_class = UserExtraSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return UserExtra.objects.filter(user=user.id)

    def create(self, request):
        user = self.request.user
        serializer = UserExtraSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # if user.is_staff:
        #     return super().create(request)
        # else:
        #     if user.id != int(request.data['user']):
        #         return Response({"error": "You can only create your own profile"}, status=status.HTTP_400_BAD_REQUEST)

        #     serializer = UserExtraSerializer(data=request.data, context={'request': request})
        #     if serializer.is_valid():
        #         serializer.save(user=user)
        #         return Response(serializer.data, status=status.HTTP_201_CREATED)
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# NEWS API VIEWS

class NewViewSet(viewsets.ModelViewSet):
    serializer_class = NewSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['category', 'ai_classification']
    search_fields = ['title']
    ordering_fields = ['created_at', 'updated_at']
    queryset = New.objects.all()

# COMMENT API VIEWS

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['content']
    ordering_fields = ['created_at', 'updated_at']
    queryset = Comment.objects.all()

    def create(self, request):
        user = self.request.user
        serializer = CommentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# NEWS IMAGE API VIEWS

class NewsImageViewSet(viewsets.ModelViewSet):
    serializer_class = NewsImageSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at']
    queryset = NewsImage.objects.all()

# CATEGORY API VIEWS

class NewsCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = NewsCategorySerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
    queryset = NewsCategory.objects.all()

# USERCATEGORY API VIEWS

class UserCategoriesViewSet(viewsets.ModelViewSet):
    serializer_class = UserCategorySerializer
    http_method_names = ['get', 'post', 'put', 'options', 'delete']
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        user_id = None
        if user_id is not None:
            #disable pagination
            #self.pagination_class = None
            serializer = UserCategorySerializer(UserCategory.objects.filter(user_extra__user=user_id), many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return UserCategory.objects.filter(user_extra__user=user)

    def create(self, request, *args, **kwargs):
        user = self.request.user
        user_extra = UserExtra.objects.get(user=user)

        try:
            category = NewsCategory.objects.get(id=request.data['category'])
        except:
            return Response({'error': "Category doesn't exists."},status=status.HTTP_400_BAD_REQUEST)

        if UserCategory.objects.filter(user_extra=user_extra, category=category).exists():
            return Response({'error': 'User already has this category.'}, status=status.HTTP_400_BAD_REQUEST)

        user_category = UserCategory.objects.create(user_extra=user_extra, category=category)
        serializer = UserCategorySerializer(user_category)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UserCategoriesDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

# CUSTOM API VIEWS

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def signin(request):

    try:
        username = request.data['username']
        password = request.data['password']
    except KeyError:
        return Response({'error': 'Missing username or password.'}, status=status.HTTP_400_BAD_REQUEST)

    if "@" in username and "." in username:
        try:
            username = User.objects.get(email=username).username
        except User.DoesNotExist:
            return Response({'error': 'Invalid credentials.'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)

    if user is not None:
        if user.is_active:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)

            user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'token': token.key,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_staff': user.is_staff,
                'is_superuser': user.is_superuser,
                'is_active': user.is_active,
                'date_joined': user.date_joined,
                'last_login': user.last_login
            }

            return Response({'user' : user_data}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'User is not active.'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Invalid credentials.'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def signup(request):
    try:
        username = request.data['username']
        email = request.data['email']
        password = request.data['password']
        first_name = request.data['first_name']
        last_name = request.data['last_name']
    except KeyError:
        return Response({
            'error': 'Missing params.',
            'params': ['username', 'email', 'password', 'first_name', 'last_name']
        }, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response({'error': 'Email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
    user.save()
    user_extra = UserExtra.objects.create(user=user)
    user_extra.save()

    return Response({'message': 'User created successfully.'}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def predict_article(request):
    try:
        text = request.data['text']
        ai_model = request.data['ai_model']
    except KeyError:
        return Response({
            'error': 'Missing params.',
            'params': [{'text': 'string'}, {'ai_model': ['LRModel']}]
        }, status=status.HTTP_400_BAD_REQUEST)

    ai_detection = AIDetection()

    if ai_model == 'LRModel':
        result = ai_detection.LRModel_Predict(text)
        return Response({'result': result}, status=status.HTTP_200_OK)
    else:
        return Response({
            'error': 'Invalid AI Model.',
            'ai_models': ['LRModel']
        }, status=status.HTTP_400_BAD_REQUEST)
