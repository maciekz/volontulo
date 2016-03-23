# -*- coding: utf-8 -*-

u"""
.. module:: api
"""
from rest_framework import viewsets

from apps.volontulo.models import Offer, Organization, UserProfile
from apps.volontulo.serializers import (
    OfferSerializer, OrganizationSerializer, UserProfileSerializer)


class UserProfileViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows UserProfiles to be viewed or edited.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class OfferViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Offers to be viewed or edited.
    """
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer


class OrganizationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows Organizations to be viewed or edited.
    """
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
