# -*- coding: utf-8 -*-

u"""
.. module:: serializers
"""
from django.contrib.auth.models import User
from rest_framework import serializers

from apps.volontulo import models


class OrganizationSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the Organization model.
    """
    class Meta:
        model = models.Organization
        fields = ('url', 'id', 'name', 'address', 'description')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the User model.
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class UserGallerySerializer(serializers.ModelSerializer):
    """
    Serializer for the UserGallery model.
    """
    class Meta:
        model = models.UserGallery
        fields = ('id', 'image', 'is_avatar')


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the UserProfile model.
    """
    user = UserSerializer(many=False)
    organizations = OrganizationSerializer(many=True)
    images = UserGallerySerializer(many=True, read_only=True)

    class Meta:
        model = models.UserProfile
        fields = ('url', 'id', 'user', 'organizations', 'is_administrator',
                  'phone_no', 'images')


class OfferImageSerializer(serializers.ModelSerializer):
    """
    Serializer for the OfferImage model.
    """
    class Meta:
        model = models.OfferImage
        fields = ('id', 'path', 'is_main')


class OfferSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the Offer model.
    """
    organization = OrganizationSerializer(many=False, read_only=True)
    volunteers = UserSerializer(many=True, read_only=True)
    images = OfferImageSerializer(many=True, read_only=True)

    class Meta:
        model = models.Offer
        fields = (
            'url', 'id', 'organization', 'volunteers', 'description',
            'requirements', 'time_commitment', 'benefits', 'location', 'title',
            'started_at', 'finished_at', 'time_period', 'status_old',
            'offer_status', 'recruitment_status', 'action_status', 'votes',
            'recruitment_start_date', 'recruitment_end_date',
            'reserve_recruitment', 'reserve_recruitment_start_date',
            'reserve_recruitment_end_date', 'action_ongoing', 'constant_coop',
            'action_start_date', 'action_end_date', 'volunteers_limit',
            'weight', 'images')


class OfferCreateSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for creation of Offers.
    """
    organization = serializers.PrimaryKeyRelatedField(
        many=False, read_only=False,
        queryset=models.Organization.objects.all())
    volunteers = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True)

    class Meta:
        model = models.Offer
        fields = (
            'url', 'id', 'organization', 'volunteers', 'description',
            'requirements', 'time_commitment', 'benefits', 'location', 'title',
            'started_at', 'finished_at', 'time_period', 'status_old',
            'offer_status', 'recruitment_status', 'action_status', 'votes',
            'recruitment_start_date', 'recruitment_end_date',
            'reserve_recruitment', 'reserve_recruitment_start_date',
            'reserve_recruitment_end_date', 'action_ongoing', 'constant_coop',
            'action_start_date', 'action_end_date', 'volunteers_limit',
            'weight')


class OfferApplySerializer(serializers.Serializer):
    """
    Serializer for applying for join to offer.
    """

    email = serializers.CharField(max_length=80)
    phone_no = serializers.CharField(max_length=80)
    fullname = serializers.CharField(max_length=80)
    comments = serializers.CharField(required=False)
