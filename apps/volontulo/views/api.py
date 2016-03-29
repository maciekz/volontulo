# -*- coding: utf-8 -*-

u"""
.. module:: api
"""
from rest_framework import generics
from rest_framework import permissions
from rest_framework import viewsets

from apps.volontulo.models import Offer, Organization, UserProfile
from apps.volontulo.serializers import (
    OfferSerializer, OfferCreateSerializer, OrganizationSerializer,
    UserProfileSerializer)


class OfferCreatePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        """
        Only authenticated users that are not admins can create new offers.
        """
        return (request.user.is_authenticated() and
                not request.user.userprofile.is_administrator)


class UserProfileViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows UserProfiles to be viewed or edited.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class OfferViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows Offers to be viewed or edited.
    """
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer


class OfferCreateView(generics.CreateAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferCreateSerializer
    permission_classes = (OfferCreatePermission, )


class OrganizationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows Organizations to be viewed or edited.
    """
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
