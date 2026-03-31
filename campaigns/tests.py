from django.contrib.admin.sites import AdminSite
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory, TestCase

from accounts.models import User

from .admin import CampaignAdmin
from .forms import CampaignForm
from .models import Campaign, Category


class CampaignFormTests(TestCase):
    def setUp(self):
        Category.objects.create(name='Medical Emergency', slug='medical-emergency')
        self.medical = Category.objects.create(name='Medical', slug='medical')
        Category.objects.create(name='Education', slug='education')

    def test_medical_emergency_is_hidden_from_campaign_category_options(self):
        form = CampaignForm()

        available_slugs = list(form.fields['category'].queryset.values_list('slug', flat=True))

        self.assertNotIn('medical-emergency', available_slugs)
        self.assertEqual(available_slugs, ['medical', 'education'])

    def test_goal_amount_and_location_are_accepted(self):
        form = CampaignForm(
            data={
                'title': 'Education Support',
                'description': 'Need help with tuition fees.',
                'goal_amount': '25000',
                'category': self.medical.pk,
                'location': 'Bengaluru',
            }
        )

        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(str(form.cleaned_data['goal_amount']), '25000')
        self.assertEqual(form.cleaned_data['location'], 'Bengaluru')


class CampaignAdminActionTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.admin_user = User.objects.create_user(
            username='adminuser',
            email='adminuser@example.com',
            password='StrongPass123!',
            role=User.Role.ADMIN,
        )
        self.category = Category.objects.create(name='Medical', slug='medical')
        self.owner = User.objects.create_user(
            username='campaigner',
            email='campaigner@example.com',
            password='StrongPass123!',
        )
        self.campaign = Campaign.objects.create(
            owner=self.owner,
            title='Help for treatment',
            description='Need urgent financial support.',
            goal_amount='50000',
            category=self.category,
            location='Mysuru',
        )
        self.admin = CampaignAdmin(Campaign, AdminSite())
        self.request = self.factory.post('/admin/campaigns/campaign/')
        self.request.user = self.admin_user

        session_middleware = SessionMiddleware(lambda request: None)
        session_middleware.process_request(self.request)
        self.request.session.save()
        setattr(self.request, '_messages', FallbackStorage(self.request))

    def test_approve_action_marks_campaign_active(self):
        self.campaign.status = Campaign.Status.REJECTED
        self.campaign.status_reason = 'Missing details'
        self.campaign.save()

        self.admin.approve_campaigns(self.request, Campaign.objects.filter(pk=self.campaign.pk))

        self.campaign.refresh_from_db()
        self.assertEqual(self.campaign.status, Campaign.Status.ACTIVE)
        self.assertTrue(self.campaign.approved)
        self.assertEqual(self.campaign.status_reason, '')

    def test_reject_action_marks_campaign_rejected(self):
        self.admin.reject_campaigns(self.request, Campaign.objects.filter(pk=self.campaign.pk))

        self.campaign.refresh_from_db()
        self.assertEqual(self.campaign.status, Campaign.Status.REJECTED)
        self.assertFalse(self.campaign.approved)
        self.assertEqual(self.campaign.status_reason, 'Rejected by admin.')
