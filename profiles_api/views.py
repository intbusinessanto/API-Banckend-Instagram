from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, filters
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated

from profiles_api import serializers, models, permissions

# Create your views here.


class HelloAPIView(APIView):
    """" API View de prueba """
    serializer_class = serializers.HelloSerializer
    
    def get(self, request, format=None):
        """ Retornar listas de caracteristicas del APIView """
        an_apiview = [
            'Usamos métodos HTTP como funciones (get, post, patch, put, delete',
            'Es similar a una vista tradicional de Django',
            'Nos da el mejor control sobre la lógica de nuestra aplicación',
            'Esta mapeado manuealmente a los URLs',
        ]

        return Response({'message': 'Hello', 'an_apiview': an_apiview })

    def post(self, request):
        """ Crea un mensaje con nuestro nombre """
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
            
    def put(self, request, pk=None):
        """ Handle updating an object """
        return Response({'method': 'PUT'})
            
    def patch(self, request, pk=None):
        """ Handle partial update of object """
        return Response({'method': 'PATCH'})
            
    def delete(self, request, pk=None):
        """ Delete an object """
        return Response({'method': 'DELETE'})
    
class HelloViewSet(viewsets.ViewSet):
    """ Test API ViewSet """
    serializer_class = serializers.HelloSerializer
    
    def list(self, request):
        """ Retornar mensaje de Hola mundo """
        
        a_viewset = [
            'Usa acciones (List, create, retrieve, update, partial_update)',
            'Automaticamente mapea a los URLs usando Routers',
            'Provee mas funcionalidad con menos codigo',
        ]
        
        return Response({'message': 'Hola', 'a_viewset': a_viewset})
    
    def create(self, request):
        """ Crear nuevo mensaje de Hola mundo """
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f"Hola {name}"
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
            
    def retrieve(self, request, pk=None):
        """ Obtiene un objeto y su ID """
        
        return Response({'http_method': 'GET'})
            
    def update(self, request, pk=None):
        """ Actualiza un objeto """
        return Response({'http_method': 'PUT'})
            
    def partial_update(self, request, pk=None):
        """ Actualiza parcialmente un objeto """ 
        return Response({'http_method': 'PATCH'})
            
    def destroy(self, request, pk=None):
        """ Destruye un objeto """
        
        return Response({'http_method': 'DELETE'})

class UserProfileViewSet(viewsets.ModelViewSet):
    """ Crear y actualizar pefiles """
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)
    

class UserLoginApiView(ObtainAuthToken):
    """ Crear tokens de autenticacion """
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    
class userProfileFeedViewSet(viewsets.ModelViewSet):
    """ Maneja el crear, leer y actualizar el profile feed """
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (
        permissions.UpdateOwnStatus,
        IsAuthenticated
    )
    
    def perform_create(self, serializer):
        """ Setear el perfil de usuario para el usuario que está logueado """
        serializer.save(user_profile=self.request.user)