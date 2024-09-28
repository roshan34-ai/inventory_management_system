from rest_framework import generics, status, views
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
from .models import Item
from .serializers import ItemSerializer, UserSerializer
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)


class UserRegistrationView(views.APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ItemListCreateView(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if cache.get('items'):
            logger.debug("Items fetched from cache")
            return cache.get('items')
        queryset = super().get_queryset()
        cache.set('items', queryset, timeout=60*15) 
        logger.debug("Items fetched from database")
        return queryset

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        cache.delete('items')
        return response


class ItemRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        item_id = kwargs.get('pk')
        cache_key = f'item_{item_id}'
        if cache.get(cache_key):
            logger.debug(f"Item {item_id} fetched from cache")
            return Response(cache.get(cache_key))
        response = super().retrieve(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=60*15)
        logger.debug(f"Item {item_id} fetched from database")
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        cache_key = f'item_{kwargs.get("pk")}'
        cache.delete(cache_key)
        cache.delete('items')
        return response

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        cache_key = f'item_{kwargs.get("pk")}'
        cache.delete(cache_key)
        cache.delete('items')
        return response
