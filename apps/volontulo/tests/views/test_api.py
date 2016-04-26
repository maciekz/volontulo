# -*- coding: utf-8 -*-

u"""
.. module:: test_api
"""
import json

from rest_framework.test import APIClient, APITestCase

from apps.volontulo.tests import common


class TestAuthenticationApi(APITestCase):
    u"""Class responsible for testing authentication API."""

    @classmethod
    def setUpTestData(cls):
        u"""Data fixtures for all tests."""
        # admin user
        cls.admin = common.initialize_administrator()

    def setUp(self):
        u"""Set up each test."""
        self.client = APIClient()

    # pylint: disable=invalid-name
    def test__login_failure(self):
        u"""Test API logging in failure."""
        response = self.client.post(
            '/rest-auth/login/', {'username': 'admin_user@example.com',
                                  'password': 'asdf'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response['Content-Type'], 'application/json')
        expected_data = {
            'non_field_errors': [
                'Podane dane uwierzytelniające nie pozwalają na zalogowanie.']}
        self.assertJSONEqual(response.content.decode('utf-8'), expected_data)

    # pylint: disable=invalid-name
    def test__login_success(self):
        u"""Test API logging in success."""
        # Log in
        response = self.client.post(
            '/rest-auth/login/', {'username': 'admin_user@example.com',
                                  'password': 'admin_password'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        json_data = json.loads(response.content.decode('utf-8'))
        self.assertTrue('key' in json_data)

    # pylint: disable=invalid-name
    def test__logout(self):
        u"""Test API logging out."""
        # Log in
        response = self.client.post(
            '/rest-auth/login/', {'username': 'admin_user@example.com',
                                  'password': 'admin_password'})
        json_data = json.loads(response.content.decode('utf-8'))
        # Use token
        token = json_data['key']
        response = self.client.post(
            '/rest-auth/logout/', HTTP_AUTHORIZATION='Token {0}'.format(token))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        expected_data = {'success': 'Successfully logged out.'}
        self.assertJSONEqual(response.content.decode('utf-8'), expected_data)


class TestOrganizationsApi(APITestCase):
    u"""Class responsible for testing organization specific API."""

    @classmethod
    def setUpTestData(cls):
        u"""Data fixtures for all tests."""
        # volunteer user - totally useless
        cls.volunteer = common.initialize_empty_volunteer()
        # organization user - no offers
        cls.organization = common.initialize_empty_organization()
        # volunteer user - offers, organizations
        cls.volunteer2, cls.organization2 = \
            common.initialize_filled_volunteer_and_organization()

    def setUp(self):
        u"""Set up each test."""
        self.client = APIClient()

    # pylint: disable=invalid-name
    def test__organizations_list(self):
        u"""Test getting organizations list JSON."""
        response = self.client.get('/api/organizations.json')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response)
        self.assertEqual(response['Content-Type'], 'application/json')
        expected_data = [
            {'url': 'http://testserver/api/organizations/1.json',
             'description': 'Organization 1 description',
             'id': 1, 'name': 'Organization 1',
             'address': 'Organization 1 address'},
            {'url': 'http://testserver/api/organizations/2.json',
             'description': '', 'id': 2, 'name': 'Organization 2',
             'address': ''}]
        self.assertJSONEqual(response.content.decode('utf-8'), expected_data)

    # pylint: disable=invalid-name
    def test__organization_details(self):
        u"""Test getting organization's details JSON."""
        response = self.client.get('/api/organizations/1.json')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response)
        self.assertEqual(response['Content-Type'], 'application/json')
        expected_data = {
            'url': 'http://testserver/api/organizations/1.json',
            'description': 'Organization 1 description',
            'id': 1, 'name': 'Organization 1',
            'address': 'Organization 1 address'}
        self.assertJSONEqual(response.content.decode('utf-8'), expected_data)


class TestUserProfilesApi(APITestCase):
    u"""Class responsible for testing user profiles specific API."""

    @classmethod
    def setUpTestData(cls):
        # volunteer user - offers, organizations
        cls.volunteer2, cls.organization2 = \
            common.initialize_filled_volunteer_and_organization()
        # admin user
        cls.admin = common.initialize_administrator()

    def setUp(self):
        u"""Set up each test."""
        self.client = APIClient()

    # pylint: disable=invalid-name
    def test__user_profiles_list(self):
        u"""Test getting user profiles list JSON."""
        response = self.client.get('/api/users_profiles.json')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response)
        self.assertEqual(response['Content-Type'], 'application/json')
        expected_data = [
            {'id': 1,
             'images': [],
             'is_administrator': False,
             'organizations': [],
             'phone_no': '',
             'url': 'http://testserver/api/users_profiles/1.json',
             'user': {'email': 'volunteer2@example.com',
                      'first_name': '',
                      'id': 1,
                      'last_name': '',
                      'username': 'volunteer2@example.com'}},
            {'id': 2,
             'images': [],
             'is_administrator': False,
             'organizations': [
                 {'address': '',
                  'description': '',
                  'id': 1,
                  'name': 'Organization 2',
                  'url': 'http://testserver/api/organizations/1.json'}],
             'phone_no': '',
             'url': 'http://testserver/api/users_profiles/2.json',
             'user': {'email': 'organization2@example.com',
                      'first_name': '',
                      'id': 2,
                      'last_name': '',
                      'username': 'organization2@example.com'}},
            {'id': 3,
             'images': [],
             'is_administrator': True,
             'organizations': [],
             'phone_no': '',
             'url': 'http://testserver/api/users_profiles/3.json',
             'user': {'email': 'admin_user@example.com',
                      'first_name': '',
                      'id': 3,
                      'last_name': '',
                      'username': 'admin_user@example.com'}}]
        self.assertJSONEqual(response.content.decode('utf-8'), expected_data)

    # pylint: disable=invalid-name
    def test__user_profile_details(self):
        u"""Test getting user profile's details JSON."""
        response = self.client.get('/api/users_profiles/1.json')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response)
        self.assertEqual(response['Content-Type'], 'application/json')
        expected_data = {
            'id': 1,
            'images': [],
            'is_administrator': False,
            'organizations': [],
            'phone_no': '',
            'url': 'http://testserver/api/users_profiles/1.json',
            'user': {'email': 'volunteer2@example.com',
                     'first_name': '',
                     'id': 1,
                     'last_name': '',
                     'username': 'volunteer2@example.com'}}
        self.assertJSONEqual(response.content.decode('utf-8'), expected_data)

    # pylint: disable=invalid-name
    def test__user_profile_admin_details(self):
        u"""Test getting admin user profile's details JSON."""
        response = self.client.get('/api/users_profiles/3.json')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response)
        self.assertEqual(response['Content-Type'], 'application/json')
        expected_data = {
            'id': 3,
            'images': [],
            'is_administrator': True,
            'organizations': [],
            'phone_no': '',
            'url': 'http://testserver/api/users_profiles/3.json',
            'user': {'email': 'admin_user@example.com',
                     'first_name': '',
                     'id': 3,
                     'last_name': '',
                     'username': 'admin_user@example.com'}}
        self.assertJSONEqual(response.content.decode('utf-8'), expected_data)


class TestOffersApi(APITestCase):
    u"""Class responsible for testing offers specific API."""

    maxDiff = None

    def setUp(self):
        u"""Set up each test."""
        # Data fixtures for all tests.
        # volunteer user - offers, organizations
        self.offer1, self.offer2 = common.initialize_filled_and_empty_offers()
        # admin user
        self.admin = common.initialize_administrator()
        # empty user
        common.initialize_empty_volunteer()
        # API client
        self.client = APIClient()

    # pylint: disable=invalid-name
    def test__offers_list(self):
        u"""Test getting offers list JSON."""
        response = self.client.get('/api/offers.json')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response)
        self.assertEqual(response['Content-Type'], 'application/json')
        expected_data = [
            {'action_end_date': None,
             'action_ongoing': False,
             'action_start_date': None,
             'action_status': 'ongoing',
             'benefits': 'Benefits 1',
             'constant_coop': False,
             'description': 'Description 1',
             'finished_at': '2015-12-12T12:13:14Z',
             'id': 1,
             'images': [],
             'location': 'Location 1',
             'offer_status': 'published',
             'organization': {
                 'address': '',
                 'description': '',
                 'id': 1,
                 'name': 'Organization 2',
                 'url': 'http://testserver/api/organizations/1.json'},
             'recruitment_end_date': None,
             'recruitment_start_date': None,
             'recruitment_status': 'open',
             'requirements': 'Requirements 1',
             'reserve_recruitment': True,
             'reserve_recruitment_end_date': None,
             'reserve_recruitment_start_date': None,
             'started_at': '2015-10-05T09:10:11Z',
             'status_old': 'ACTIVE',
             'time_commitment': 'Time commitment 1',
             'time_period': 'Time period 1',
             'title': 'Title 1',
             'url': 'http://testserver/api/offers/1.json',
             'volunteers': [{'email': 'volunteer2@example.com',
                             'first_name': '',
                             'id': 1,
                             'last_name': '',
                             'username': 'volunteer2@example.com'}],
             'volunteers_limit': 0,
             'votes': True,
             'weight': 0},
            {'action_end_date': None,
             'action_ongoing': False,
             'action_start_date': None,
             'action_status': 'ongoing',
             'benefits': 'Benefits 2',
             'constant_coop': False,
             'description': 'Description 2',
             'finished_at': '2015-12-12T12:13:14Z',
             'id': 2,
             'images': [],
             'location': 'Location 2',
             'offer_status': 'published',
             'organization': {
                 'address': '',
                 'description': '',
                 'id': 1,
                 'name': 'Organization 2',
                 'url': 'http://testserver/api/organizations/1.json'},
             'recruitment_end_date': None,
             'recruitment_start_date': None,
             'recruitment_status': 'open',
             'requirements': 'Requirements 2',
             'reserve_recruitment': True,
             'reserve_recruitment_end_date': None,
             'reserve_recruitment_start_date': None,
             'started_at': '2015-10-05T09:10:11Z',
             'status_old': 'ACTIVE',
             'time_commitment': 'Time commitment 2',
             'time_period': 'Time period 2',
             'title': 'Title 2',
             'url': 'http://testserver/api/offers/2.json',
             'volunteers': [],
             'volunteers_limit': 0,
             'votes': True,
             'weight': 0}]
        self.assertJSONEqual(response.content.decode('utf-8'), expected_data)

    def test__offers_list_for_user_id(self):
        u"""Test getting offers list JSON for user."""
        response = self.client.get('/api/offers.json?user_id=1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response)
        self.assertEqual(response['Content-Type'], 'application/json')
        expected_data = [
            {'action_end_date': None,
             'action_ongoing': False,
             'action_start_date': None,
             'action_status': 'ongoing',
             'benefits': 'Benefits 1',
             'constant_coop': False,
             'description': 'Description 1',
             'finished_at': '2015-12-12T12:13:14Z',
             'id': 1,
             'images': [],
             'location': 'Location 1',
             'offer_status': 'published',
             'organization': {
                 'address': '',
                 'description': '',
                 'id': 1,
                 'name': 'Organization 2',
                 'url': 'http://testserver/api/organizations/1.json'},
             'recruitment_end_date': None,
             'recruitment_start_date': None,
             'recruitment_status': 'open',
             'requirements': 'Requirements 1',
             'reserve_recruitment': True,
             'reserve_recruitment_end_date': None,
             'reserve_recruitment_start_date': None,
             'started_at': '2015-10-05T09:10:11Z',
             'status_old': 'ACTIVE',
             'time_commitment': 'Time commitment 1',
             'time_period': 'Time period 1',
             'title': 'Title 1',
             'url': 'http://testserver/api/offers/1.json',
             'volunteers': [{'email': 'volunteer2@example.com',
                             'first_name': '',
                             'id': 1,
                             'last_name': '',
                             'username': 'volunteer2@example.com'}],
             'volunteers_limit': 0,
             'votes': True,
             'weight': 0}, ]
        self.assertJSONEqual(response.content.decode('utf-8'), expected_data)

    # pylint: disable=invalid-name
    def test__offer_details(self):
        u"""Test getting offer's details JSON."""
        response = self.client.get('/api/offers/2.json')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response)
        self.assertEqual(response['Content-Type'], 'application/json')
        expected_data = {
            'action_end_date': None,
            'action_ongoing': False,
            'action_start_date': None,
            'action_status': 'ongoing',
            'benefits': 'Benefits 2',
            'constant_coop': False,
            'description': 'Description 2',
            'finished_at': '2015-12-12T12:13:14Z',
            'id': 2,
            'images': [],
            'location': 'Location 2',
            'offer_status': 'published',
            'organization': {
                'address': '',
                'description': '',
                'id': 1,
                'name': 'Organization 2',
                'url': 'http://testserver/api/organizations/1.json'},
            'recruitment_end_date': None,
            'recruitment_start_date': None,
            'recruitment_status': 'open',
            'requirements': 'Requirements 2',
            'reserve_recruitment': True,
            'reserve_recruitment_end_date': None,
            'reserve_recruitment_start_date': None,
            'started_at': '2015-10-05T09:10:11Z',
            'status_old': 'ACTIVE',
            'time_commitment': 'Time commitment 2',
            'time_period': 'Time period 2',
            'title': 'Title 2',
            'url': 'http://testserver/api/offers/2.json',
            'volunteers': [],
            'volunteers_limit': 0,
            'votes': True,
            'weight': 0}
        self.assertJSONEqual(response.content.decode('utf-8'), expected_data)

    # pylint: disable=invalid-name
    def test__offer_create_failure_anonymous(self):
        u"""Test creating offer API failure - not logged in."""
        response = self.client.post(
            '/api/offers/create/', {
                'title': 'API created offer',
                'time_commitment': 'API time commitment',
                'benefits': 'API benefits',
                'location': 'API location',
                'description': 'API description',
                'organization': '1',
            })
        self.assertEqual(response.status_code, 401)  # Unauthorized
        self.assertEqual(response['Content-Type'], 'application/json')
        expected_data = {'detail': 'Nie podano danych uwierzytelniających.'}
        self.assertJSONEqual(response.content.decode('utf-8'), expected_data)

    # pylint: disable=invalid-name
    def test__offer_create_failure_admin(self):
        u"""Test creating offer API failure - admin."""
        # Log in
        response = self.client.post(
            '/rest-auth/login/', {'username': 'admin_user@example.com',
                                  'password': 'admin_password'})
        json_data = json.loads(response.content.decode('utf-8'))
        # Use token
        token = json_data['key']
        # Create offer using token
        response = self.client.post(
            '/api/offers/create/', {
                'title': 'API created offer',
                'time_commitment': 'API time commitment',
                'benefits': 'API benefits',
                'location': 'API location',
                'description': 'API description',
                'organization': '1',
            },
            HTTP_AUTHORIZATION='Token {0}'.format(token))
        self.assertEqual(response.status_code, 400)  # Bad Request
        self.assertEqual(response['Content-Type'], 'application/json')
        expected_data = {
            'info': 'Administrator nie może tworzyć nowych ofert.'}
        self.assertJSONEqual(response.content.decode('utf-8'), expected_data)

    # pylint: disable=invalid-name
    def test__offer_create_success(self):
        u"""Test creating offer API success."""
        # Log in
        response = self.client.post(
            '/rest-auth/login/', {'username': 'organization2@example.com',
                                  'password': 'organization2'})
        json_data = json.loads(response.content.decode('utf-8'))
        # Use token
        token = json_data['key']
        # Create offer using token
        response = self.client.post(
            '/api/offers/create/', {
                'title': 'API created offer',
                'time_commitment': 'API time commitment',
                'benefits': 'API benefits',
                'location': 'API location',
                'description': 'API description',
                'organization': '1',
            },
            HTTP_AUTHORIZATION='Token {0}'.format(token))
        self.assertEqual(response.status_code, 201)  # Created
        self.assertEqual(response['Content-Type'], 'application/json')
        expected_data = {
            'action_end_date': None,
            'action_ongoing': False,
            'action_start_date': None,
            'action_status': 'ongoing',
            'benefits': 'API benefits',
            'constant_coop': False,
            'description': 'API description',
            'finished_at': None,
            'id': 3,
            'location': 'API location',
            'offer_status': 'unpublished',
            'organization': 1,
            'recruitment_end_date': None,
            'recruitment_start_date': None,
            'recruitment_status': 'open',
            'requirements': '',
            'reserve_recruitment': False,
            'reserve_recruitment_end_date': None,
            'reserve_recruitment_start_date': None,
            'started_at': None,
            'status_old': 'NEW',
            'time_commitment': 'API time commitment',
            'time_period': '',
            'title': 'API created offer',
            'url': 'http://testserver/api/offers/3/',
            'volunteers': [],
            'volunteers_limit': 0,
            'votes': False,
            'weight': 0}
        self.assertJSONEqual(response.content.decode('utf-8'), expected_data)

    # pylint: disable=invalid-name
    def test__offer_full_edit_failure_anonymous(self):
        u"""Test editing offer API (full) failure - not logged in."""
        response = self.client.put(
            '/api/offers/2/update/', {
                'title': 'API created offer updated',
                'time_commitment': 'API time commitment updated',
                'benefits': 'API benefits updated',
                'location': 'API location updated',
                'description': 'API description updated',
                'organization': '1',
            })
        self.assertEqual(response.status_code, 401)  # Unauthorized
        self.assertEqual(response['Content-Type'], 'application/json')
        expected_data = {'detail': 'Nie podano danych uwierzytelniających.'}
        self.assertJSONEqual(response.content.decode('utf-8'), expected_data)

    # pylint: disable=invalid-name
    def test__offer_partial_edit_failure_anonymous(self):
        u"""Test editing offer API (partial) failure - not logged in."""
        response = self.client.patch(
            '/api/offers/2/update/', {
                'title': 'API created offer updated',
            })
        self.assertEqual(response.status_code, 401)  # Unauthorized
        self.assertEqual(response['Content-Type'], 'application/json')
        expected_data = {'detail': 'Nie podano danych uwierzytelniających.'}
        self.assertJSONEqual(response.content.decode('utf-8'), expected_data)

    # pylint: disable=invalid-name
    def test__offer_full_edit_failure_wrong_user(self):
        u"""Test editig offer API (full) failure - wrong user."""
        # Log in
        response = self.client.post(
            '/rest-auth/login/', {'username': 'volunteer1@example.com',
                                  'password': 'volunteer1'})
        json_data = json.loads(response.content.decode('utf-8'))
        # Use token
        token = json_data['key']
        # Edit offer using token
        response = self.client.put(
            '/api/offers/2/update/', {
                'title': 'API created offer updated',
                'time_commitment': 'API time commitment updated',
                'benefits': 'API benefits updated',
                'location': 'API location updated',
                'description': 'API description updated',
                'organization': '1',
            },
            HTTP_AUTHORIZATION='Token {0}'.format(token))
        self.assertEqual(response.status_code, 404)  # Not Found
        self.assertEqual(response['Content-Type'], 'application/json')
        expected_data = {
            'info': 'Użytkownik nie może edytować wybranej oferty.'}
        self.assertJSONEqual(response.content.decode('utf-8'), expected_data)

    # pylint: disable=invalid-name
    def test__offer_partial_edit_failure_wrong_user(self):
        u"""Test editig offer API (partial) failure - wrong user."""
        # Log in
        response = self.client.post(
            '/rest-auth/login/', {'username': 'volunteer1@example.com',
                                  'password': 'volunteer1'})
        json_data = json.loads(response.content.decode('utf-8'))
        # Use token
        token = json_data['key']
        # Edit offer using token
        response = self.client.patch(
            '/api/offers/2/update/', {
                'title': 'API created offer updated',
            },
            HTTP_AUTHORIZATION='Token {0}'.format(token))
        self.assertEqual(response.status_code, 404)  # Not Found
        self.assertEqual(response['Content-Type'], 'application/json')
        expected_data = {
            'info': 'Użytkownik nie może edytować wybranej oferty.'}
        self.assertJSONEqual(response.content.decode('utf-8'), expected_data)

    # pylint: disable=invalid-name
    def test__offer_full_edit_success_user(self):
        u"""Test editing offer API (full) success - user."""
        # Log in
        response = self.client.post(
            '/rest-auth/login/', {'username': 'organization2@example.com',
                                  'password': 'organization2'})
        json_data = json.loads(response.content.decode('utf-8'))
        # Use token
        token = json_data['key']
        # Edit offer using token
        response = self.client.put(
            '/api/offers/2/update/', {
                'title': 'API edited offer updated',
                'time_commitment': 'API time commitment updated',
                'benefits': 'API benefits updated',
                'location': 'API location updated',
                'description': 'API description updated',
                'organization': '1',
            },
            HTTP_AUTHORIZATION='Token {0}'.format(token))
        self.assertEqual(response.status_code, 200)  # OK
        self.assertEqual(response['Content-Type'], 'application/json')
        expected_data = {
            'action_end_date': None,
            'action_ongoing': False,
            'action_start_date': None,
            'action_status': 'ongoing',
            'benefits': 'API benefits updated',
            'constant_coop': False,
            'description': 'API description updated',
            'finished_at': '2015-12-12T12:13:14Z',
            'id': 2,
            'location': 'API location updated',
            'offer_status': 'unpublished',
            'organization': 1,
            'recruitment_end_date': None,
            'recruitment_start_date': None,
            'recruitment_status': 'open',
            'requirements': 'Requirements 2',
            'reserve_recruitment': False,
            'reserve_recruitment_end_date': None,
            'reserve_recruitment_start_date': None,
            'started_at': '2015-10-05T09:10:11Z',
            'status_old': 'ACTIVE',
            'time_commitment': 'API time commitment updated',
            'time_period': 'Time period 2',
            'title': 'API edited offer updated',
            'url': 'http://testserver/api/offers/2/',
            'volunteers': [],
            'volunteers_limit': 0,
            'votes': False,
            'weight': 0}
        self.assertJSONEqual(response.content.decode('utf-8'), expected_data)

    def test__offer_partial_edit_success_user(self):
        u"""Test editing offer API (partial) success - user."""
        # Log in
        response = self.client.post(
            '/rest-auth/login/', {'username': 'organization2@example.com',
                                  'password': 'organization2'})
        json_data = json.loads(response.content.decode('utf-8'))
        # Use token
        token = json_data['key']
        # Edit offer using token
        response = self.client.patch(
            '/api/offers/2/update/', {
                'title': 'API edited offer updated',
                'location': 'API location updated',
            },
            HTTP_AUTHORIZATION='Token {0}'.format(token))
        self.assertEqual(response.status_code, 200)  # OK
        self.assertEqual(response['Content-Type'], 'application/json')
        expected_data = {
            'action_end_date': None,
            'action_ongoing': False,
            'action_start_date': None,
            'action_status': 'ongoing',
            'benefits': 'Benefits 2',
            'constant_coop': False,
            'description': 'Description 2',
            'finished_at': '2015-12-12T12:13:14Z',
            'id': 2,
            'location': 'API location updated',
            'offer_status': 'unpublished',
            'organization': 1,
            'recruitment_end_date': None,
            'recruitment_start_date': None,
            'recruitment_status': 'open',
            'requirements': 'Requirements 2',
            'reserve_recruitment': True,
            'reserve_recruitment_end_date': None,
            'reserve_recruitment_start_date': None,
            'started_at': '2015-10-05T09:10:11Z',
            'status_old': 'ACTIVE',
            'time_commitment': 'Time commitment 2',
            'time_period': 'Time period 2',
            'title': 'API edited offer updated',
            'url': 'http://testserver/api/offers/2/',
            'volunteers': [],
            'volunteers_limit': 0,
            'votes': True,
            'weight': 0}
        self.assertJSONEqual(response.content.decode('utf-8'), expected_data)

    # pylint: disable=invalid-name
    def test__offer_full_edit_success_admin(self):
        u"""Test editing offer API (full) success - admin."""
        # Log in
        response = self.client.post(
            '/rest-auth/login/', {'username': 'admin_user@example.com',
                                  'password': 'admin_password'})
        json_data = json.loads(response.content.decode('utf-8'))
        # Use token
        token = json_data['key']
        # Edit offer using token
        response = self.client.put(
            '/api/offers/2/update/', {
                'title': 'API edited offer updated',
                'time_commitment': 'API time commitment updated',
                'benefits': 'API benefits updated',
                'location': 'API location updated',
                'description': 'API description updated',
                'organization': '1',
            },
            HTTP_AUTHORIZATION='Token {0}'.format(token))
        self.assertEqual(response.status_code, 200)  # OK
        self.assertEqual(response['Content-Type'], 'application/json')
        expected_data = {
            'action_end_date': None,
            'action_ongoing': False,
            'action_start_date': None,
            'action_status': 'ongoing',
            'benefits': 'API benefits updated',
            'constant_coop': False,
            'description': 'API description updated',
            'finished_at': '2015-12-12T12:13:14Z',
            'id': 2,
            'location': 'API location updated',
            'offer_status': 'unpublished',
            'organization': 1,
            'recruitment_end_date': None,
            'recruitment_start_date': None,
            'recruitment_status': 'open',
            'requirements': 'Requirements 2',
            'reserve_recruitment': False,
            'reserve_recruitment_end_date': None,
            'reserve_recruitment_start_date': None,
            'started_at': '2015-10-05T09:10:11Z',
            'status_old': 'ACTIVE',
            'time_commitment': 'API time commitment updated',
            'time_period': 'Time period 2',
            'title': 'API edited offer updated',
            'url': 'http://testserver/api/offers/2/',
            'volunteers': [],
            'volunteers_limit': 0,
            'votes': False,
            'weight': 0}
        self.assertJSONEqual(response.content.decode('utf-8'), expected_data)

    def test__offer_partial_edit_success_admin(self):
        u"""Test editing offer API (partial) success - admin."""
        # Log in
        response = self.client.post(
            '/rest-auth/login/', {'username': 'admin_user@example.com',
                                  'password': 'admin_password'})
        json_data = json.loads(response.content.decode('utf-8'))
        # Use token
        token = json_data['key']
        # Edit offer using token
        response = self.client.patch(
            '/api/offers/2/update/', {
                'title': 'API edited offer updated',
                'location': 'API location updated',
            },
            HTTP_AUTHORIZATION='Token {0}'.format(token))
        self.assertEqual(response.status_code, 200)  # OK
        self.assertEqual(response['Content-Type'], 'application/json')
        expected_data = {
            'action_end_date': None,
            'action_ongoing': False,
            'action_start_date': None,
            'action_status': 'ongoing',
            'benefits': 'Benefits 2',
            'constant_coop': False,
            'description': 'Description 2',
            'finished_at': '2015-12-12T12:13:14Z',
            'id': 2,
            'location': 'API location updated',
            'offer_status': 'unpublished',
            'organization': 1,
            'recruitment_end_date': None,
            'recruitment_start_date': None,
            'recruitment_status': 'open',
            'requirements': 'Requirements 2',
            'reserve_recruitment': True,
            'reserve_recruitment_end_date': None,
            'reserve_recruitment_start_date': None,
            'started_at': '2015-10-05T09:10:11Z',
            'status_old': 'ACTIVE',
            'time_commitment': 'Time commitment 2',
            'time_period': 'Time period 2',
            'title': 'API edited offer updated',
            'url': 'http://testserver/api/offers/2/',
            'volunteers': [],
            'volunteers_limit': 0,
            'votes': True,
            'weight': 0}
        self.assertJSONEqual(response.content.decode('utf-8'), expected_data)

    # pylint: disable=invalid-name
    def test__offer_join_failure_anonymous(self):
        u"""Test joining offer API failure - not logged in."""
        response = self.client.post(
            '/api/offers/2/join/', {
                'email': 'organization2@example.com',
                'phone_no': '123',
                'fullname': 'Organization 2 User',
                'comments': 'This is a comment',
            })
        self.assertEqual(response.status_code, 401)  # Unauthorized
        self.assertEqual(response['Content-Type'], 'application/json')
        expected_data = {'detail': 'Nie podano danych uwierzytelniających.'}
        self.assertJSONEqual(response.content.decode('utf-8'), expected_data)

    def test__offer_join_failure_missing_data(self):
        u"""Test joining offer API failure - missing data."""
        # Log in
        response = self.client.post(
            '/rest-auth/login/', {'username': 'organization2@example.com',
                                  'password': 'organization2'})
        json_data = json.loads(response.content.decode('utf-8'))
        # Use token
        token = json_data['key']
        # Join offer using token
        response = self.client.post(
            '/api/offers/2/join/', {
                'email': 'organization2@example.com',
                'fullname': 'Organization 2 User',
                'comments': 'This is a comment',
            },
            HTTP_AUTHORIZATION='Token {0}'.format(token))
        self.assertEqual(response.status_code, 400)  # Bad Request
        self.assertEqual(response['Content-Type'], 'application/json')
        expected_data = {
            "phone_no": ["To pole jest wymagane."]
        }
        self.assertJSONEqual(response.content.decode('utf-8'), expected_data)

    def test__offer_join_success(self):
        u"""Test joining offer API success."""
        # Log in
        response = self.client.post(
            '/rest-auth/login/', {'username': 'organization2@example.com',
                                  'password': 'organization2'})
        json_data = json.loads(response.content.decode('utf-8'))
        # Use token
        token = json_data['key']
        # Join offer using token
        response = self.client.post(
            '/api/offers/2/join/', {
                'email': 'organization2@example.com',
                'phone_no': '123',
                'fullname': 'Organization 2 User',
                'comments': 'This is a comment',
            },
            HTTP_AUTHORIZATION='Token {0}'.format(token))
        self.assertEqual(response.status_code, 200)  # OK
        self.assertEqual(response['Content-Type'], 'application/json')
        expected_data = {
            'info': 'Zgłoszenie chęci uczestnictwa zostało wysłane.'}
        self.assertJSONEqual(response.content.decode('utf-8'), expected_data)

    def test__offer_join_failure_already_applied(self):
        u"""Test joining offer API failure - user already applied."""
        # Log in
        response = self.client.post(
            '/rest-auth/login/', {'username': 'organization2@example.com',
                                  'password': 'organization2'})
        json_data = json.loads(response.content.decode('utf-8'))
        # Use token
        token = json_data['key']
        # Join offer using token
        response = self.client.post(
            '/api/offers/2/join/', {
                'email': 'organization2@example.com',
                'phone_no': '123',
                'fullname': 'Organization 2 User',
                'comments': 'This is a comment',
            },
            HTTP_AUTHORIZATION='Token {0}'.format(token))
        self.assertEqual(response.status_code, 200)  # OK
        self.assertEqual(response['Content-Type'], 'application/json')
        expected_data = {
            'info': 'Zgłoszenie chęci uczestnictwa zostało wysłane.'}
        self.assertJSONEqual(response.content.decode('utf-8'), expected_data)
        # Try to join again
        response = self.client.post(
            '/api/offers/2/join/', {
                'email': 'organization2@example.com',
                'phone_no': '123',
                'fullname': 'Organization 2 User',
                'comments': 'This is a comment',
            },
            HTTP_AUTHORIZATION='Token {0}'.format(token))
        self.assertEqual(response.status_code, 400)  # Bad Request
        self.assertEqual(response['Content-Type'], 'application/json')
        expected_data = {
            'info': 'Już wyraziłeś chęć uczestnictwa w tej ofercie.'}
        self.assertJSONEqual(response.content.decode('utf-8'), expected_data)
