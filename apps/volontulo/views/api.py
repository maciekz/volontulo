# -*- coding: utf-8 -*-

u"""
.. module:: api
"""
from rest_framework import permissions
from rest_framework import viewsets

from apps.volontulo.models import Offer, Organization, UserProfile
from apps.volontulo.serializers import (
    OfferSerializer, OrganizationSerializer, UserProfileSerializer)


class UserOfferPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        """
        All users can list and retrieve offers
        but only authenticated users can create new ones.
        """
        if view.action in ('list', 'retrieve'):
            return True
        elif view.action == 'create':
            return (request.user.is_authenticated() and
                    not request.user.userprofile.is_administrator)
        else:
            return False


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
    permission_classes = (UserOfferPermission, )


class OrganizationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows Organizations to be viewed or edited.
    """
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
