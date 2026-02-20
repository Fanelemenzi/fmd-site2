"""
API views for outbreaks.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Q
from .models import Outbreak, DipTank, CordonLine, FootWashStation
from .serializers import OutbreakSerializer, OutbreakListSerializer


class OutbreakViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for viewing outbreaks.
    
    Provides:
    - List all outbreaks
    - Retrieve single outbreak details
    - Filter by status, region
    - GeoJSON export for map rendering
    - Statistics summary
    """
    queryset = Outbreak.objects.filter(is_active=True, is_verified=True)
    serializer_class = OutbreakSerializer
    
    def get_serializer_class(self):
        """Use simplified serializer for list views."""
        if self.action == 'list':
            return OutbreakListSerializer
        return OutbreakSerializer
    
    def get_queryset(self):
        """
        Filter queryset based on query parameters.
        
        Supported filters:
        - status: active, surveillance, cleared
        - region: hhohho, manzini, lubombo, shiselweni
        """
        queryset = super().get_queryset()
        
        # Filter by status
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by region
        region_filter = self.request.query_params.get('region', None)
        if region_filter:
            queryset = queryset.filter(region=region_filter)
        
        return queryset.order_by('-date_reported')
    
    @action(detail=False, methods=['get'])
    def geojson(self, request):
        """
        Return outbreaks in GeoJSON format for map rendering.
        
        Usage: GET /api/outbreaks/geojson/
        
        Accepts same filters as list endpoint (status, region).
        """
        queryset = self.get_queryset()
        
        features = [outbreak.to_geojson_feature() for outbreak in queryset]
        
        geojson = {
            "type": "FeatureCollection",
            "features": features
        }
        
        return Response(geojson)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """
        Return summary statistics about outbreaks.
        
        Usage: GET /api/outbreaks/statistics/
        """
        queryset = self.get_queryset()
        
        # Count by status
        stats_by_status = queryset.values('status').annotate(
            count=Count('id')
        ).order_by('status')
        
        # Count by region
        stats_by_region = queryset.values('region').annotate(
            count=Count('id')
        ).order_by('region')
        
        # Total animals affected
        total_affected = sum(outbreak.animals_affected for outbreak in queryset)
        total_quarantined = sum(outbreak.animals_quarantined for outbreak in queryset)
        
        statistics = {
            "total_outbreaks": queryset.count(),
            "active_outbreaks": queryset.filter(status='active').count(),
            "surveillance_zones": queryset.filter(status='surveillance').count(),
            "cleared_outbreaks": queryset.filter(status='cleared').count(),
            "total_animals_affected": total_affected,
            "total_animals_quarantined": total_quarantined,
            "by_status": list(stats_by_status),
            "by_region": list(stats_by_region),
        }
        
        return Response(statistics)


class DipTankViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for viewing dip tanks.
    
    Provides:
    - List all dip tanks
    - Retrieve single dip tank details
    - Filter by region, affected status
    - GeoJSON export for map rendering
    """
    queryset = DipTank.objects.filter(is_active=True)
    
    def get_queryset(self):
        """
        Filter queryset based on query parameters.
        
        Supported filters:
        - region: hhohho, manzini, lubombo, shiselweni
        - affected: true, false
        """
        queryset = super().get_queryset()
        
        # Filter by region
        region_filter = self.request.query_params.get('region', None)
        if region_filter:
            queryset = queryset.filter(region=region_filter)
        
        # Filter by affected status
        affected_filter = self.request.query_params.get('affected', None)
        if affected_filter is not None:
            is_affected = affected_filter.lower() == 'true'
            queryset = queryset.filter(is_affected=is_affected)
        
        return queryset.order_by('region', 'name')
    
    def list(self, request, *args, **kwargs):
        """Return simplified list of dip tanks."""
        queryset = self.get_queryset()
        
        data = []
        for dip_tank in queryset:
            data.append({
                'id': dip_tank.id,
                'name': dip_tank.name,
                'region': dip_tank.region,
                'region_display': dip_tank.get_region_display(),
                'is_affected': dip_tank.is_affected,
                'latitude': float(dip_tank.latitude),
                'longitude': float(dip_tank.longitude),
                'capacity': dip_tank.capacity,
            })
        
        return Response({
            'count': len(data),
            'results': data
        })
    
    @action(detail=False, methods=['get'])
    def geojson(self, request):
        """
        Return dip tanks in GeoJSON format for map rendering.
        
        Usage: GET /api/diptanks/geojson/
        
        Accepts same filters as list endpoint (region, affected).
        """
        queryset = self.get_queryset()
        
        features = [dip_tank.to_geojson_feature() for dip_tank in queryset]
        
        geojson = {
            "type": "FeatureCollection",
            "features": features
        }
        
        return Response(geojson)


class CordonLineViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for viewing cordon lines.
    
    Provides:
    - List all cordon lines
    - Retrieve single cordon line details
    - Filter by region, status
    - GeoJSON export for map rendering
    """
    queryset = CordonLine.objects.filter(is_active=True)
    
    def get_queryset(self):
        """
        Filter queryset based on query parameters.
        
        Supported filters:
        - region: hhohho, manzini, lubombo, shiselweni
        - status: active, inactive, temporary
        """
        queryset = super().get_queryset()
        
        # Filter by region
        region_filter = self.request.query_params.get('region', None)
        if region_filter:
            queryset = queryset.filter(region=region_filter)
        
        # Filter by status
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset.order_by('-date_established')
    
    def list(self, request, *args, **kwargs):
        """Return simplified list of cordon lines."""
        queryset = self.get_queryset()
        
        data = []
        for cordon_line in queryset:
            data.append({
                'id': cordon_line.id,
                'name': cordon_line.name,
                'region': cordon_line.region,
                'region_display': cordon_line.get_region_display(),
                'status': cordon_line.status,
                'status_display': cordon_line.get_status_display(),
                'date_established': cordon_line.date_established.isoformat(),
                'date_expires': cordon_line.date_expires.isoformat() if cordon_line.date_expires else None,
                'description': cordon_line.description,
            })
        
        return Response({
            'count': len(data),
            'results': data
        })
    
    @action(detail=False, methods=['get'])
    def geojson(self, request):
        """
        Return cordon lines in GeoJSON format for map rendering.
        
        Usage: GET /api/cordonlines/geojson/
        
        Accepts same filters as list endpoint (region, status).
        """
        queryset = self.get_queryset()
        
        features = [cordon_line.to_geojson_feature() for cordon_line in queryset]
        
        geojson = {
            "type": "FeatureCollection",
            "features": features
        }
        
        return Response(geojson)


class FootWashStationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for viewing foot wash stations.
    
    Provides:
    - List all foot wash stations
    - Retrieve single station details
    - Filter by region, road type, operational status
    - GeoJSON export for map rendering
    """
    queryset = FootWashStation.objects.filter(is_active=True)
    
    def get_queryset(self):
        """
        Filter queryset based on query parameters.
        
        Supported filters:
        - region: hhohho, manzini, lubombo, shiselweni
        - road_type: highway, main_road, secondary_road, border_crossing
        - operational: true, false
        """
        queryset = super().get_queryset()
        
        # Filter by region
        region_filter = self.request.query_params.get('region', None)
        if region_filter:
            queryset = queryset.filter(region=region_filter)
        
        # Filter by road type
        road_type_filter = self.request.query_params.get('road_type', None)
        if road_type_filter:
            queryset = queryset.filter(road_type=road_type_filter)
        
        # Filter by operational status
        operational_filter = self.request.query_params.get('operational', None)
        if operational_filter is not None:
            is_operational = operational_filter.lower() == 'true'
            queryset = queryset.filter(is_operational=is_operational)
        
        return queryset.order_by('region', 'road_name', 'name')
    
    def list(self, request, *args, **kwargs):
        """Return simplified list of foot wash stations."""
        queryset = self.get_queryset()
        
        data = []
        for station in queryset:
            data.append({
                'id': station.id,
                'name': station.name,
                'region': station.region,
                'region_display': station.get_region_display(),
                'road_name': station.road_name,
                'road_type': station.road_type,
                'road_type_display': station.get_road_type_display(),
                'latitude': float(station.latitude),
                'longitude': float(station.longitude),
                'is_operational': station.is_operational,
                'operating_hours': station.operating_hours,
                'contact_phone': station.contact_phone,
            })
        
        return Response({
            'count': len(data),
            'results': data
        })
    
    @action(detail=False, methods=['get'])
    def geojson(self, request):
        """
        Return foot wash stations in GeoJSON format for map rendering.
        
        Usage: GET /api/footwashstations/geojson/
        
        Accepts same filters as list endpoint (region, road_type, operational).
        """
        queryset = self.get_queryset()
        
        features = [station.to_geojson_feature() for station in queryset]
        
        geojson = {
            "type": "FeatureCollection",
            "features": features
        }
        
        return Response(geojson)