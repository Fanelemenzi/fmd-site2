"""
Views for frontend pages.
"""
from django.shortcuts import render
from django.views.generic import TemplateView
from outbreaks.models import Outbreak
from updates.models import Update


class HomeView(TemplateView):
    """Home page with map and statistics."""
    template_name = 'pages/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get active outbreaks for map
        context['active_outbreaks'] = Outbreak.objects.filter(
            is_active=True,
            is_verified=True,
            status='active'
        ).count()
        
        # Get surveillance zones
        context['surveillance_zones'] = Outbreak.objects.filter(
            is_active=True,
            is_verified=True,
            status='surveillance'
        ).count()
        
        # Get cleared outbreaks
        context['cleared_outbreaks'] = Outbreak.objects.filter(
            is_active=True,
            is_verified=True,
            status='cleared'
        ).count()
        
        # Get total animals affected
        all_outbreaks = Outbreak.objects.filter(is_active=True, is_verified=True)
        context['total_animals_affected'] = sum(
            outbreak.animals_affected for outbreak in all_outbreaks
        )
        
        # Get featured updates
        context['featured_updates'] = Update.objects.filter(
            is_published=True,
            is_featured=True
        )[:3]
        
        return context


class AboutView(TemplateView):
    """About FMD page."""
    template_name = 'pages/about.html'


class UpdatesView(TemplateView):
    """Updates and news list page."""
    template_name = 'pages/updates.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['updates'] = Update.objects.filter(is_published=True)[:20]
        return context


class ControlMeasuresView(TemplateView):
    """Control measures and guidelines page."""
    template_name = 'pages/control_measures.html'


class ContactView(TemplateView):
    """Contact information page."""
    template_name = 'pages/contact.html'