from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import  HelloApiView, HelloViewSet

router = DefaultRouter()
router.register('hello-viewset', HelloViewSet, base_name='hello-viewset')

urlpatterns = [
    path('hello-view', HelloApiView.as_view(), name='hello'),
    path('', include(router.urls)),
]