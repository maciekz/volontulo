# -*- coding: utf-8 -*-

u"""
.. module:: api
"""
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from apps.volontulo.models import Offer, Organization, UserProfile
from apps.volontulo.serializers import (
    OfferSerializer, OfferCreateSerializer, OrganizationSerializer,
    UserProfileSerializer)
from apps.volontulo.views.offers import (
    get_offers_list, offer_post_creation_actions)


# pylint: disable=too-many-ancestors
class UserProfileViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows UserProfiles to be viewed.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


# pylint: disable=too-many-ancestors
class OfferViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows Offers to be viewed.
    """
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer

    def list(self, request, *args, **kwargs):
        queryset = get_offers_list(request)
        user_id = request.query_params.get('user_id', None)
        if user_id is not None:
            queryset = queryset.filter(volunteers__id=user_id)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class OfferCreateView(generics.CreateAPIView):
    """
    API endpoint that allows Offers to be created.
    """
    queryset = Offer.objects.all()
    serializer_class = OfferCreateSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        # Only authenticated users that are not admins can create new offers.
        if request.user.userprofile.is_administrator:
            data = {u'info':
                    u"Administrator nie może tworzyć nowych ofert."}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        # You have to have at least a single organization
        organizations = request.user.userprofile.organizations.all()
        if not organizations.exists():
            data = {u'info':
                    u"Nie masz jeszcze żadnej założonej organizacji "
                    u"na volontuloapp.org."}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)


class OfferUpdateView(generics.UpdateAPIView):
    """
    API endpoint that allows Offers to be updated.
    """
    queryset = Offer.objects.all()
    serializer_class = OfferCreateSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def _check_perms(self, request, *args, **kwargs):
        """
        Check if user has permission to edit an offer.
        """
        try:
            is_edit_allowed = request.user.userprofile.can_edit_offer(
                offer_id=kwargs['pk'])
        except Offer.DoesNotExist:
            is_edit_allowed = False
        return is_edit_allowed

    def update(self, request, *args, **kwargs):
        is_edit_allowed = self._check_perms(request, *args, **kwargs)
        if not is_edit_allowed:
            data = {u'info':
                    u"Użytkownik nie może edytować wybranej oferty."}
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        return super().update(request, *args, **kwargs)


# pylint: disable=too-many-ancestors
class OrganizationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows Organizations to be viewed or edited.
    """
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
