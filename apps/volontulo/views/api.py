# -*- coding: utf-8 -*-

u"""
.. module:: api
"""
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from apps.volontulo.lib.email import send_mail
from apps.volontulo.models import Offer, Organization, UserProfile
from apps.volontulo.serializers import (
    OfferApplySerializer, OfferSerializer, OfferCreateSerializer,
    OrganizationSerializer, UserProfileSerializer)
from apps.volontulo.views.offers import (
    check_offer_edit_perms, get_offers_list, offer_post_creation_actions,
    offer_post_edit_actions, offer_post_join_actions)


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

    # pylint: disable=unused-argument
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

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        offer = self.perform_create(serializer)
        offer_post_creation_actions(request, offer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    def perform_create(self, serializer):
        return serializer.save()


class OfferUpdateView(generics.UpdateAPIView):
    """
    API endpoint that allows Offers to be updated.
    """
    queryset = Offer.objects.all()
    serializer_class = OfferCreateSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def update(self, request, *args, **kwargs):
        is_edit_allowed = check_offer_edit_perms(request, kwargs['pk'])
        if not is_edit_allowed:
            data = {u'info':
                    u"Użytkownik nie może edytować wybranej oferty."}
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        # Unpublish offer and save history
        offer = Offer.objects.get(pk=kwargs['pk'])
        offer_post_edit_actions(request, offer)
        return super().update(request, *args, **kwargs)


class OfferJoinView(generics.GenericAPIView):
    """
    API endpoint that allows Offers to be joined.
    """
    permission_classes = (permissions.IsAuthenticated, )

    # pylint: disable=unused-argument
    def post(self, request, *args, **kwargs):
        # Check if data is valid
        serializer = OfferApplySerializer(data=request.data)
        serializer.is_valid()
        if serializer.errors:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        # Check if user hasn't applied yet
        id_ = kwargs['pk']
        user = request.user
        has_applied = Offer.objects.filter(
            volunteers=user,
            volunteers__offer=id_,
        ).count()
        if has_applied:
            data = {u'info':
                    u'Już wyraziłeś chęć uczestnictwa w tej ofercie.'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        # Add user to volunteers
        offer = Offer.objects.get(id=id_)
        offer.volunteers.add(user)
        offer.save()
        offer_post_join_actions(request, offer, user, request.data)

        data = {u'info':
                u'Zgłoszenie chęci uczestnictwa zostało wysłane.'}
        return Response(data, status=status.HTTP_200_OK)


# pylint: disable=too-many-ancestors
class UserCreatedOfferViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows to view Offers created by user.
    """
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer

    # pylint: disable=unused-argument
    def list(self, request, *args, **kwargs):
        creator_id = kwargs['pk']
        queryset = Offer.objects.filter(
            organization__userprofiles__user__id=creator_id)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


# pylint: disable=too-many-ancestors
class OrganizationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows Organizations to be viewed or edited.
    """
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
