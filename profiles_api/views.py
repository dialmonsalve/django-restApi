from rest_framework import status, viewsets, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated

from profiles_api import serializers
from .models import UserProfile, ProfileFeedItem
from .permissions import UpdateOwnProfile, UpdateOwnStatus

# Create your views here.
class HelloApiView(APIView):
    '''Test API View'''
    
    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        '''Returns a list of APIView features'''
        an_apiview = [
            'Uses HTTP methods as functions(get, post, patch, put, delete)',
            'Is similar to a traditional Django View',
            'Gives you the most control over you application logic',
            'Is mapped mannually to URLs'
        ]
        
        return Response({'message':'Hello', 'an_apiview': an_apiview})
    
    def post(self, request):
        '''Create a hello message with our name'''
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            name = serializer.validated_data.get('name') # type: ignore
            message = f'Hello {name}'
            return Response({'message':message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, pk=None):
        '''Handle updating an object'''
        return Response({'method':'PUT'})

    def patch(self, request, pk=None):
        '''Handle a partial update an object'''
        return Response({'method':'PATCH'})

    def delete(self, request, pk=None):
        '''Delete an object'''
        return Response({'method':'DELETE'})
    

class HelloViewSet(viewsets.ViewSet):
    '''Test Api viewSet'''
    serializer_class = serializers.HelloSerializer

    def list(self, request):
        '''Return a hello message'''
        
        an_viewset = [
            'Uses actions(list, create, retrieve, update, partial_update, destroy)',
            'Automatically maps to URLs using Routers',
            'Provides more functionality with less code',
            'Is mapped mannually to URLs'
        ]
        return Response({'message':'Hello', 'an_iviewset': an_viewset})
    
    def create(self, request):
        '''Create a hello message'''
        serializer = self.serializer_class(data=request.data) # type: ignore
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        name = serializer.validated_data.get('name') # type: ignore
        message = f'Hello {name}'

        return Response({'message':message})
    
    def retrieve(self, request, pk=None):
        '''Handle getting an object by its ID'''
        return Response({'http_method':'GET'})
    
    def update(self, request, pk=None):
        '''Handle updating an object'''
        return Response({'http_method':'PUT'})
    
    def partial_update(self, request, pk=None):
        '''Handle a partial update an object'''
        return Response({'http_method':'PATCH'})
    
    def destroy(self, request, pk=None):
        '''Delete an object'''
        return Response({'http_method':'DELETE'})
    
class UserProfileViewSet(viewsets.ModelViewSet):
    '''Handle creating and updating profiles'''
    serializer_class = serializers.UserProfileSerializer
    queryset = UserProfile.objects.all()
    authentication_classes = (TokenAuthentication, )
    permission_classes = (UpdateOwnProfile, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', 'email', )
    
class UserLoginApiView(ObtainAuthToken):
    '''Handel creating user authentication tokens'''
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    
class UserProfileFeedViewSet(viewsets.ModelViewSet):
    '''Handles creating, reading and updating profile feed items'''
    authentication_classes = (TokenAuthentication, )
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = ProfileFeedItem.objects.all()
    permission_classes = ( UpdateOwnStatus, IsAuthenticated )
    
    def perform_create(self, serializer):
        '''return the user profile to the logged in user'''
        serializer.save(user_profile=self.request.user)
        # return super().perform_create(serializer)