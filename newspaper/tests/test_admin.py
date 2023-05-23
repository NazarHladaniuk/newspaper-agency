from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from django.urls import reverse


class AdminSiteTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="pass12345"
            )
        self.client.force_login(self.admin_user)
        self.redactor = get_user_model().objects.create_user(
            username="redactor",
            password="pass12345",
            years_of_experience=3,
        )

    def test_redactor_experience_listed(self):
        url = reverse("admin:newspaper_redactor_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.redactor.years_of_experience)

    def test_redactor_detailed_experience_listed(self):
        url = reverse("admin:newspaper_redactor_change", args=[self.redactor.id])
        response = self.client.get(url)

        self.assertContains(response, self.redactor.years_of_experience)
