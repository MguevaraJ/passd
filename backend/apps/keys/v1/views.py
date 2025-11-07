from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.keys.v1.serializers import (
    KeyItemSerializer, 
    FolderSerializer, 
    TagSerializer,
    OrganizedKeysSerializer
)
from apps.keys.bo.items_bo import ItemsBO, FolderBO

class KeyItemViewSet(viewsets.ModelViewSet):
    serializer_class = KeyItemSerializer

    def get_queryset(self):
        return ItemsBO.list_items(user=self.request.user)

    @action(detail=True, methods=['patch'], url_path='tags')
    def update_tags(self, request, pk=None):
        item = self.get_object()
        serializer = TagSerializer(instance=item, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_item = serializer.save()
        return Response(KeyItemSerializer(updated_item).data)

    @action(detail=False, methods=['get'], url_path='organized')
    def get_organized(self, request):
        """
        Retorna todas las keys organizadas por carpetas y las keys sin carpeta.
        """
        organized_data = ItemsBO.get_organized_keys(user=request.user)
        serializer = OrganizedKeysSerializer(organized_data)
        return Response(serializer.data)

class FolderViewSet(viewsets.ModelViewSet):
    serializer_class = FolderSerializer

    def get_queryset(self):
        return FolderBO.list_folders(user=self.request.user)

    @action(detail=True, methods=['post'], url_path='add-item')
    def add_keyitem(self, request, pk=None):
        folder = self.get_object()
        serializer = KeyItemSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        item = serializer.save(user=self.request.user, folder=folder)
        return Response(KeyItemSerializer(item).data, status=status.HTTP_201_CREATED)

