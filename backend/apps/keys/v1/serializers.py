from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.keys.models import KeyItem, Folder
from apps.keys.bo.items_bo import ItemsBO, FolderBO

User = get_user_model()

class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ['id', 'name', 'user']
        read_only_fields = ['id', 'user']

    def create(self, validated_data):
        user = self.context['request'].user
        return FolderBO.create_folder(user=user, **validated_data)

class TagSerializer(serializers.Serializer):
    tags = serializers.CharField()

    def update(self, instance, validated_data):
        return ItemsBO.update_item(instance, tags=validated_data.get('tags', ''))

class KeyItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyItem
        fields = ['id', 'url', 'username', 'encrypted_pass', 'note', 'tags', 'folder', 'user']
        read_only_fields = ['id', 'user']

    def create(self, validated_data):
        user = self.context['request'].user
        return ItemsBO.create_item(user=user, **validated_data)

    def update(self, instance, validated_data):
        return ItemsBO.update_item(instance, **validated_data)
