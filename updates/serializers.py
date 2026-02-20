"""
Serializers for the updates API.
"""
from rest_framework import serializers
from .models import Update


class UpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for Update model.
    """
    update_type_display = serializers.CharField(source='get_update_type_display', read_only=True)
    
    class Meta:
        model = Update
        fields = [
            'id',
            'title',
            'content',
            'update_type',
            'update_type_display',
            'related_outbreak',
            'published_at',
            'updated_at',
            'source',
            'image',
            'document',
            'is_featured',
        ]
        read_only_fields = ['id', 'updated_at']


class UpdateListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for list views.
    """
    update_type_display = serializers.CharField(source='get_update_type_display', read_only=True)
    content_preview = serializers.SerializerMethodField()
    
    class Meta:
        model = Update
        fields = [
            'id',
            'title',
            'content_preview',
            'update_type',
            'update_type_display',
            'published_at',
            'source',
            'is_featured',
        ]
    
    def get_content_preview(self, obj):
        """Return first 200 characters of content."""
        return obj.content[:200] + '...' if len(obj.content) > 200 else obj.content