from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Company, KBEntry, QueryLog


class TeamBoardAPITests(APITestCase):

    def setUp(self):
        self.register_url = '/api/auth/register/'
        self.login_url = '/api/auth/login/'
        self.query_url = '/api/kb/query/'
        self.usage_url = '/api/admin/usage-summary/'

        KBEntry.objects.create(
            question='How does Django ORM work?',
            answer='Django ORM provides database access using Python objects.',
            category='framework'
        )

    def test_register_company(self):
        response = self.client.post(
            self.register_url,
            {
                'username': 'testclient',
                'email': 'client@example.com',
                'password': 'TestPassword123!',
                'company_name': 'Test Company'
            },
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertTrue(
            User.objects.filter(username='testclient').exists()
        )

        user = User.objects.get(username='testclient')

        self.assertEqual(
            user.company.company_name,
            'Test Company'
        )

        self.assertTrue(
            user.company.api_key
        )

    def test_login(self):
        user = User.objects.create_user(
            username='loginuser',
            email='login@example.com',
            password='TestPassword123!'
        )

        response = self.client.post(
            self.login_url,
            {
                'username': 'loginuser',
                'password': 'TestPassword123!'
            },
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertIn('access', response.data)

    def test_kb_query_requires_authentication(self):
        response = self.client.post(
            self.query_url,
            {
                'search': 'Django'
            },
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_authenticated_kb_query_creates_log(self):
        user = User.objects.create_user(
            username='queryuser',
            email='query@example.com',
            password='TestPassword123!'
        )

        self.client.force_authenticate(user=user)

        response = self.client.post(
            self.query_url,
            {
                'search': 'Django'
            },
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data['count'],
            1
        )

        self.assertEqual(
            QueryLog.objects.count(),
            1
        )

        self.assertEqual(
            QueryLog.objects.first().search_term,
            'Django'
        )

    def test_client_cannot_access_usage_summary(self):
        user = User.objects.create_user(
            username='clientuser',
            email='client@example.com',
            password='TestPassword123!'
        )

        self.client.force_authenticate(user=user)

        response = self.client.get(self.usage_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_admin_can_access_usage_summary(self):
        user = User.objects.create_user(
            username='adminuser',
            email='admin@example.com',
            password='TestPassword123!'
        )

        user.company.role = Company.Role.ADMIN
        user.company.save()

        self.client.force_authenticate(user=user)

        response = self.client.get(self.usage_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertIn(
            'total_queries',
            response.data
        )

        self.assertIn(
            'active_companies',
            response.data
        )

        self.assertIn(
            'top_search_terms',
            response.data
        )