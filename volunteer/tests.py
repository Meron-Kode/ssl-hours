from decimal import Decimal
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import VolunteerLog


class VolunteerLogModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_str_representation(self):
        log = VolunteerLog.objects.create(
            student=self.user,
            organization_name='Food Bank',
            volunteer_date='2024-01-15',
            hours_worked=Decimal('3.50'),
            supervisor_name='Jane Doe',
            supervisor_email='jane@example.com',
            reflection='I learned a lot.',
        )
        self.assertEqual(str(log), 'testuser - Food Bank (3.50 hrs)')

    def test_default_status_is_pending(self):
        log = VolunteerLog.objects.create(
            student=self.user,
            organization_name='Library',
            volunteer_date='2024-02-01',
            hours_worked=Decimal('2.00'),
            supervisor_name='Bob Smith',
            supervisor_email='bob@example.com',
            reflection='Helped organize books.',
        )
        self.assertEqual(log.status, 'P')

    def test_status_choices(self):
        log = VolunteerLog(
            student=self.user,
            organization_name='Test Org',
            volunteer_date='2024-03-01',
            hours_worked=Decimal('1.00'),
            supervisor_name='Supervisor',
            supervisor_email='sup@example.com',
            reflection='Test reflection.',
            status='A',
        )
        self.assertEqual(log.get_status_display(), 'Approved')


class DashboardViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='student', password='pass123')

    def test_dashboard_redirects_anonymous_user(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response['Location'])

    def test_dashboard_accessible_when_logged_in(self):
        self.client.login(username='student', password='pass123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_shows_correct_totals(self):
        self.client.login(username='student', password='pass123')
        VolunteerLog.objects.create(
            student=self.user,
            organization_name='Org A',
            volunteer_date='2024-01-10',
            hours_worked=Decimal('10.00'),
            supervisor_name='Sup A',
            supervisor_email='a@example.com',
            reflection='Reflection A.',
            status='A',
        )
        VolunteerLog.objects.create(
            student=self.user,
            organization_name='Org B',
            volunteer_date='2024-02-10',
            hours_worked=Decimal('5.00'),
            supervisor_name='Sup B',
            supervisor_email='b@example.com',
            reflection='Reflection B.',
            status='P',
        )
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.context['total_hours'], Decimal('10.00'))
        self.assertEqual(response.context['goal'], 75)

    def test_dashboard_progress_capped_at_100(self):
        self.client.login(username='student', password='pass123')
        VolunteerLog.objects.create(
            student=self.user,
            organization_name='Org',
            volunteer_date='2024-01-01',
            hours_worked=Decimal('100.00'),
            supervisor_name='Sup',
            supervisor_email='s@example.com',
            reflection='Reflection.',
            status='A',
        )
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.context['progress_percentage'], 100)


class AddLogViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='student2', password='pass123')

    def test_add_log_redirects_anonymous_user(self):
        response = self.client.get(reverse('add_log'))
        self.assertEqual(response.status_code, 302)

    def test_add_log_get_shows_form(self):
        self.client.login(username='student2', password='pass123')
        response = self.client.get(reverse('add_log'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'organization_name')

    def test_add_log_post_creates_entry(self):
        self.client.login(username='student2', password='pass123')
        response = self.client.post(reverse('add_log'), {
            'organization_name': 'Animal Shelter',
            'volunteer_date': '2024-03-15',
            'hours_worked': '4.50',
            'supervisor_name': 'Mary Jones',
            'supervisor_email': 'mary@shelter.org',
            'reflection': 'I helped care for animals.',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))
        log = VolunteerLog.objects.get(organization_name='Animal Shelter')
        self.assertEqual(log.student, self.user)
        self.assertEqual(log.status, 'P')
