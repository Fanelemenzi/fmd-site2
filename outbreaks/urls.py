"""
URL routing for outbreaks API.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OutbreakViewSet, DipTankViewSet, CordonLineViewSet, FootWashStationViewSet

router = DefaultRouter()
router.register(r'outbreaks', OutbreakViewSet, basename='outbreak')
router.register(r'diptanks', DipTankViewSet, basename='diptank')
router.register(r'cordonlines', CordonLineViewSet, basename='cordonline')
router.register(r'footwashstations', FootWashStationViewSet, basename='footwashstation')

urlpatterns = [
    path('', include(router.urls)),
]