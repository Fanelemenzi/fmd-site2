"""
Models for updates, news, and announcements.
"""
from django.db import models
from django.utils import timezone


class Update(models.Model):
    """
    Represents news, announcements, and official updates
    related to FMD control and management.
    """
    
    UPDATE_TYPE_CHOICES = [
        ('news', 'News'),
        ('announcement', 'Official Announcement'),
        ('guideline', 'Control Measure / Guideline'),
        ('alert', 'Alert / Warning'),
    ]
    
    # Basic Information
    title = models.CharField(
        max_length=200,
        help_text="Title of the update"
    )
    content = models.TextField(
        help_text="Full content of the update"
    )
    update_type = models.CharField(
        max_length=20,
        choices=UPDATE_TYPE_CHOICES,
        default='news'
    )
    
    # Optional link to related outbreak
    related_outbreak = models.ForeignKey(
        'outbreaks.Outbreak',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='updates',
        help_text="Link to a specific outbreak if relevant"
    )
    
    # Dates
    published_at = models.DateTimeField(
        default=timezone.now,
        help_text="When this update was published"
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )
    
    # Source
    source = models.CharField(
        max_length=200,
        help_text="Source of the update",
        default="Ministry of Agriculture"
    )
    
    # Media
    image = models.ImageField(
        upload_to='updates/images/',
        null=True,
        blank=True,
        help_text="Optional image for the update"
    )
    document = models.FileField(
        upload_to='updates/documents/',
        null=True,
        blank=True,
        help_text="Optional document attachment (PDF, etc.)"
    )
    
    # Admin fields
    is_published = models.BooleanField(
        default=True,
        help_text="Is this update visible to the public?"
    )
    is_featured = models.BooleanField(
        default=False,
        help_text="Feature this update on the homepage?"
    )
    
    class Meta:
        ordering = ['-published_at']
        verbose_name = "Update"
        verbose_name_plural = "Updates"
    
    def __str__(self):
        return f"{self.title} ({self.get_update_type_display()})"