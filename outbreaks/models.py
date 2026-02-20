"""
Models for disease outbreak tracking.
"""
from django.db import models
from django.utils import timezone


class Outbreak(models.Model):
    """
    Represents a Foot and Mouth Disease outbreak location.
    
    For production with PostGIS, replace the latitude/longitude fields
    with a GeoDjango PointField for better geospatial querying.
    """
    
    STATUS_CHOICES = [
        ('active', 'Active Outbreak'),
        ('surveillance', 'Under Surveillance'),
        ('cleared', 'Cleared/Controlled'),
    ]
    
    REGION_CHOICES = [
        ('hhohho', 'Hhohho'),
        ('manzini', 'Manzini'),
        ('lubombo', 'Lubombo'),
        ('shiselweni', 'Shiselweni'),
    ]
    
    # Basic Information
    title = models.CharField(
        max_length=200,
        help_text="Brief title for the outbreak (e.g., 'Manzini Region Outbreak - Jan 2024')"
    )
    description = models.TextField(
        help_text="Detailed description of the outbreak"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )
    region = models.CharField(
        max_length=50,
        choices=REGION_CHOICES
    )
    
    # Location (simplified for development)
    # For production, use: location = models.PointField() with PostGIS
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        help_text="Latitude coordinate"
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        help_text="Longitude coordinate"
    )
    location_name = models.CharField(
        max_length=200,
        help_text="Name of the specific location/farm"
    )
    
    # Outbreak Details
    animals_affected = models.PositiveIntegerField(
        default=0,
        help_text="Number of animals affected"
    )
    animals_quarantined = models.PositiveIntegerField(
        default=0,
        help_text="Number of animals under quarantine"
    )
    
    # Dates
    date_reported = models.DateTimeField(
        default=timezone.now,
        help_text="When the outbreak was first reported"
    )
    date_confirmed = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When the outbreak was officially confirmed"
    )
    date_cleared = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When the outbreak was declared cleared"
    )
    last_updated = models.DateTimeField(
        auto_now=True
    )
    
    # Source and Attribution
    source = models.CharField(
        max_length=200,
        help_text="Source of the outbreak information",
        default="Ministry of Agriculture"
    )
    
    # Admin fields
    is_verified = models.BooleanField(
        default=False,
        help_text="Has this outbreak been verified by authorities?"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Is this record active in the system?"
    )
    
    class Meta:
        ordering = ['-date_reported']
        verbose_name = "Outbreak"
        verbose_name_plural = "Outbreaks"
    
    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"
    
    def to_geojson_feature(self):
        """
        Convert outbreak to GeoJSON feature format for map rendering.
        """
        return {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [float(self.longitude), float(self.latitude)]
            },
            "properties": {
                "id": self.id,
                "title": self.title,
                "description": self.description,
                "status": self.status,
                "status_display": self.get_status_display(),
                "region": self.region,
                "region_display": self.get_region_display(),
                "location_name": self.location_name,
                "animals_affected": self.animals_affected,
                "animals_quarantined": self.animals_quarantined,
                "date_reported": self.date_reported.isoformat(),
                "last_updated": self.last_updated.isoformat(),
                "source": self.source,
            }
        }


class CordonLine(models.Model):
    """
    Represents cordon lines used to control cattle movement during FMD outbreaks.
    """
    
    REGION_CHOICES = [
        ('hhohho', 'Hhohho'),
        ('manzini', 'Manzini'),
        ('lubombo', 'Lubombo'),
        ('shiselweni', 'Shiselweni'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('temporary', 'Temporary'),
    ]
    
    # Basic Information
    name = models.CharField(
        max_length=200,
        help_text="Name/description of the cordon line"
    )
    region = models.CharField(
        max_length=50,
        choices=REGION_CHOICES
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )
    
    # Line coordinates (stored as JSON)
    # Format: [{"lat": -26.123, "lng": 31.456}, {"lat": -26.124, "lng": 31.457}, ...]
    coordinates = models.JSONField(
        help_text="Array of coordinate points defining the cordon line"
    )
    
    # Details
    description = models.TextField(
        blank=True,
        help_text="Purpose and details of this cordon line"
    )
    restrictions = models.TextField(
        blank=True,
        help_text="Movement restrictions and regulations"
    )
    
    # Dates
    date_established = models.DateTimeField(
        default=timezone.now,
        help_text="When this cordon line was established"
    )
    date_expires = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When this cordon line expires (if temporary)"
    )
    
    # Admin fields
    is_active = models.BooleanField(
        default=True,
        help_text="Is this cordon line currently active?"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date_established']
        verbose_name = "Cordon Line"
        verbose_name_plural = "Cordon Lines"
    
    def __str__(self):
        return f"{self.name} ({self.get_region_display()}) - {self.get_status_display()}"
    
    def to_geojson_feature(self):
        """Convert cordon line to GeoJSON feature format for map rendering."""
        return {
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": [[point["lng"], point["lat"]] for point in self.coordinates]
            },
            "properties": {
                "id": self.id,
                "name": self.name,
                "region": self.region,
                "region_display": self.get_region_display(),
                "status": self.status,
                "status_display": self.get_status_display(),
                "description": self.description,
                "restrictions": self.restrictions,
                "date_established": self.date_established.isoformat(),
                "date_expires": self.date_expires.isoformat() if self.date_expires else None,
            }
        }


class FootWashStation(models.Model):
    """
    Represents foot wash stations on major roads for FMD prevention.
    """
    
    REGION_CHOICES = [
        ('hhohho', 'Hhohho'),
        ('manzini', 'Manzini'),
        ('lubombo', 'Lubombo'),
        ('shiselweni', 'Shiselweni'),
    ]
    
    ROAD_TYPE_CHOICES = [
        ('highway', 'Highway'),
        ('main_road', 'Main Road'),
        ('secondary_road', 'Secondary Road'),
        ('border_crossing', 'Border Crossing'),
    ]
    
    # Basic Information
    name = models.CharField(
        max_length=200,
        help_text="Name of the foot wash station location"
    )
    region = models.CharField(
        max_length=50,
        choices=REGION_CHOICES
    )
    road_name = models.CharField(
        max_length=200,
        help_text="Name of the road where station is located"
    )
    road_type = models.CharField(
        max_length=20,
        choices=ROAD_TYPE_CHOICES,
        default='main_road'
    )
    
    # Location
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        help_text="Latitude coordinate"
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        help_text="Longitude coordinate"
    )
    
    # Instructions and procedures
    instructions = models.TextField(
        help_text="Step-by-step instructions for using this station"
    )
    operating_hours = models.CharField(
        max_length=100,
        default="24/7",
        help_text="Operating hours of the station"
    )
    contact_person = models.CharField(
        max_length=200,
        blank=True,
        help_text="Contact person at this station"
    )
    contact_phone = models.CharField(
        max_length=20,
        blank=True,
        help_text="Contact phone number"
    )
    
    # Status
    is_operational = models.BooleanField(
        default=True,
        help_text="Is this station currently operational?"
    )
    last_maintenance = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Last maintenance date"
    )
    
    # Admin fields
    is_active = models.BooleanField(
        default=True,
        help_text="Is this station active in the system?"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['region', 'road_name', 'name']
        verbose_name = "Foot Wash Station"
        verbose_name_plural = "Foot Wash Stations"
    
    def __str__(self):
        return f"{self.name} - {self.road_name} ({self.get_region_display()})"
    
    def to_geojson_feature(self):
        """Convert foot wash station to GeoJSON feature format for map rendering."""
        return {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [float(self.longitude), float(self.latitude)]
            },
            "properties": {
                "id": self.id,
                "name": self.name,
                "region": self.region,
                "region_display": self.get_region_display(),
                "road_name": self.road_name,
                "road_type": self.road_type,
                "road_type_display": self.get_road_type_display(),
                "instructions": self.instructions,
                "operating_hours": self.operating_hours,
                "contact_person": self.contact_person,
                "contact_phone": self.contact_phone,
                "is_operational": self.is_operational,
                "last_maintenance": self.last_maintenance.isoformat() if self.last_maintenance else None,
            }
        }


class DipTank(models.Model):
    """
    Represents a dip tank location for livestock treatment.
    Used to show affected areas with 5km radius circles.
    """
    
    REGION_CHOICES = [
        ('hhohho', 'Hhohho'),
        ('manzini', 'Manzini'),
        ('lubombo', 'Lubombo'),
        ('shiselweni', 'Shiselweni'),
    ]
    
    # Basic Information
    name = models.CharField(
        max_length=200,
        help_text="Name of the dip tank location"
    )
    region = models.CharField(
        max_length=50,
        choices=REGION_CHOICES
    )
    
    # Location
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        help_text="Latitude coordinate"
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        help_text="Longitude coordinate"
    )
    
    # Status
    is_affected = models.BooleanField(
        default=False,
        help_text="Is this dip tank area affected by FMD?"
    )
    
    # Additional details
    capacity = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Number of animals this dip tank can serve"
    )
    last_inspection = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Last inspection date"
    )
    notes = models.TextField(
        blank=True,
        help_text="Additional notes about this dip tank"
    )
    
    # Admin fields
    is_active = models.BooleanField(
        default=True,
        help_text="Is this dip tank active in the system?"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['region', 'name']
        verbose_name = "Dip Tank"
        verbose_name_plural = "Dip Tanks"
    
    def __str__(self):
        status = "Affected" if self.is_affected else "Clear"
        return f"{self.name} ({self.get_region_display()}) - {status}"
    
    def to_geojson_feature(self):
        """
        Convert dip tank to GeoJSON feature format for map rendering.
        """
        return {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [float(self.longitude), float(self.latitude)]
            },
            "properties": {
                "id": self.id,
                "name": self.name,
                "region": self.region,
                "region_display": self.get_region_display(),
                "is_affected": self.is_affected,
                "capacity": self.capacity,
                "last_inspection": self.last_inspection.isoformat() if self.last_inspection else None,
                "notes": self.notes,
                "radius": 5000,  # 5km radius in meters
            }
        }