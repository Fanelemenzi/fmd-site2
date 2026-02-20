"""
Serializers for the outbreaks API.
"""
from rest_framework import serializers
from .models import Outbreak


class OutbreakSerializer(serializers.ModelSerializer):
    """
    Serializer for Outbreak model with all fields.
    """
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    region_display = serializers.CharField(source='get_region_display', read_only=True)
    
    class Meta:
        model = Outbreak
        fields = [
            'id',
            'title',
            'description',
            'status',
            'status_display',
            'region',
            'region_display',
            'latitude',
            'longitude',
            'location_name',
            'animals_affected',
            'animals_quarantined',
            'date_reported',
            'date_confirmed',
            'date_cleared',
            'last_updated',
            'source',
            'is_verified',
        ]
        read_only_fields = ['id', 'last_updated']


class OutbreakListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for list views with essential fields only.
    """
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    region_display = serializers.CharField(source='get_region_display', read_only=True)
    
    class Meta:
        model = Outbreak
        fields = [
            'id',
            'title',
            'status',
            'status_display',
            'region',
            'region_display',
            'location_name',
            'animals_affected',
            'date_reported',
            'last_updated',
        ]