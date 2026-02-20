"""
API views for updates.
"""
from rest_framework import viewsets
from .models import Update
from .serializers import UpdateSerializer, UpdateListSerializer


class UpdateViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for viewing updates and news.
    
    Provides:
    - List all updates
    - Retrieve single update details
    - Filter by type
    """
    queryset = Update.objects.filter(is_published=True)
    serializer_class = UpdateSerializer
    
    def get_serializer_class(self):
        """Use simplified serializer for list views."""
        if self.action == 'list':
            return UpdateListSerializer
        return UpdateSerializer
    
    def get_queryset(self):
        """
        Filter queryset based on query parameters.
        
        Supported filters:
        - type: news, announcement, guideline, alert
        - featured: true/false
        """
        queryset = super().get_queryset()
        
        # Filter by update type
        update_type = self.request.query_params.get('type', None)
        if update_type:
            queryset = queryset.filter(update_type=update_type)
        
        # Filter featured updates
        featured = self.request.query_params.get('featured', None)
        if featured and featured.lower() == 'true':
            queryset = queryset.filter(is_featured=True)
        
        return queryset.order_by('-published_at')