from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.test import TestCase
from django.urls import reverse

from .models import SupportTicket


class LoginPageSiteTests(TestCase):
    def test_login_page_loads_even_if_site_record_is_missing(self):
        Site.objects.all().delete()

        response = self.client.get(reverse('login'))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Site.objects.filter(id=1).exists())


class SupportTicketWorkflowTests(TestCase):
    def setUp(self):
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_user(
            username='requester',
            email='requester@example.com',
            password='StrongPass123!'
        )
        self.admin = self.user_model.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='StrongPass123!',
            role=self.user_model.Role.ADMIN
        )
        self.ticket = SupportTicket.objects.create(
            user=self.user,
            subject='Verification pending',
            category=SupportTicket.Category.VERIFICATION,
            message='Please verify my submitted documents.'
        )

    def test_admin_dashboard_uses_admin_section_layout(self):
        self.client.force_login(self.admin)
        response = self.client.get(reverse('admin_dashboard'))

        self.assertContains(response, 'Admin Control Center')
        self.assertNotContains(response, 'User Portal')

    def test_admin_can_update_ticket_status_and_solution(self):
        self.client.force_login(self.admin)

        response = self.client.post(
            reverse('resolve_ticket', args=[self.ticket.pk]),
            {
                'status': SupportTicket.Status.IN_PROGRESS,
                'admin_notes': 'We are reviewing the documents and will update you shortly.',
            },
            follow=True,
        )

        self.ticket.refresh_from_db()

        self.assertEqual(self.ticket.status, SupportTicket.Status.IN_PROGRESS)
        self.assertEqual(
            self.ticket.admin_notes,
            'We are reviewing the documents and will update you shortly.',
        )
        self.assertContains(response, 'We are reviewing the documents and will update you shortly.')

    def test_resolved_ticket_is_cleared_from_active_admin_queue(self):
        self.client.force_login(self.admin)

        self.client.post(
            reverse('resolve_ticket', args=[self.ticket.pk]),
            {
                'status': SupportTicket.Status.RESOLVED,
                'admin_notes': 'Issue solved and cleared from the queue.',
            },
            follow=True,
        )
        response = self.client.get(reverse('admin_dashboard'))

        self.assertEqual(list(response.context['open_tickets']), [])
        self.assertContains(response, 'All caught up! No support tickets yet.')
        self.assertNotContains(response, 'Issue solved and cleared from the queue.')

    def test_user_ticket_dashboard_shows_issue_details_and_solution(self):
        self.ticket.status = SupportTicket.Status.RESOLVED
        self.ticket.admin_notes = 'Your documents were verified successfully.'
        self.ticket.save()

        self.client.force_login(self.user)
        response = self.client.get(reverse('my_tickets'))

        self.assertContains(response, 'Please verify my submitted documents.')
        self.assertContains(response, 'Your documents were verified successfully.')

    def test_admin_dashboard_lists_resolved_ticket_details(self):
        self.ticket.status = SupportTicket.Status.RESOLVED
        self.ticket.admin_notes = 'Resolved after confirming the uploaded proof.'
        self.ticket.save()

        self.client.force_login(self.admin)
        response = self.client.get(reverse('admin_dashboard'))

        self.assertContains(response, 'Please verify my submitted documents.')
        self.assertContains(response, 'Resolved after confirming the uploaded proof.')
        self.assertContains(response, self.ticket.get_status_display())
