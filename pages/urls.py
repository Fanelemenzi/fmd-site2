"""
URL routing for frontend pages.
"""
from django.urls import path
from .views import (
    HomeView,
    AboutView,
    UpdatesView,
    ControlMeasuresView,
    ContactView
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('updates/', UpdatesView.as_view(), name='updates'),
    path('control-measures/', ControlMeasuresView.as_view(), name='control_measures'),
    path('contact/', ContactView.as_view(), name='contact'),
]