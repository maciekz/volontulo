# -*- coding: utf-8 -*-

u"""
.. module:: serializers
"""
from django.contrib.auth.models import User
from rest_framework import serializers

from apps.volontulo.models import Offer, Organization, UserProfile


class OrganizationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Organization
        fields = ('url', 'id', 'name', 'address', 'description')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(many=False)
    organizations = OrganizationSerializer(many=True)

    class Meta:
        model = UserProfile
        fields = ('url', 'id', 'user', 'organizations', 'is_administrator',
                  'phone_no')


class OfferSerializer(serializers.HyperlinkedModelSerializer):
    organization = OrganizationSerializer(many=False)
    volunteers = UserSerializer(many=True)

    class Meta:
        model = Offer
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

