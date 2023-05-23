from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from newspaper.forms import RedactorInfoUpdateForm
from newspaper.models import Redactor

REDACTOR_LIST_URL = reverse("newspaper:redactor-list")
REDACTOR_CREATE_URL = reverse("newspaper:redactor-create")


class PublicRedactorListTest(TestCase):
    def test_login_required(self):
        expected_redirect_url = reverse("login") + "?next=" + REDACTOR_LIST_URL
        response = self.client.get(REDACTOR_LIST_URL)
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, expected_redirect_url)


class PrivateRedactorListTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_name", password="test_password"
        )
        self.client.force_login(self.user)
        self.redactor1 = Redactor.objects.create(
            username="redactor1", first_name="John", last_name="Doe"
        )
        self.redactor2 = Redactor.objects.create(
            username="redactor2", first_name="Jane", last_name="Smith"
        )

    def test_retrieve_redactor_list(self):
        response = self.client.get(REDACTOR_LIST_URL)
        redactors = Redactor.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["redactor_list"]), list(redactors))
        self.assertTemplateUsed(response, "newspaper/redactor_list.html")

    def test_redactor_list_search(self):
        redactor_queryset = Redactor.objects.filter(username__icontains="redactor1")
        response = self.client.get(REDACTOR_LIST_URL + "?username=redactor1")

        self.assertEqual(
            list(response.context["redactor_list"]),
            list(redactor_queryset),
        )

        self.assertTemplateUsed(response, "newspaper/redactor_list.html")

    def test_redactor_list_search_empty(self):
        response = self.client.get(REDACTOR_LIST_URL + "?username=unknown")

        self.assertEqual(
            list(response.context["redactor_list"]),
            [],
        )

        self.assertTemplateUsed(response, "newspaper/redactor_list.html")


class PublicRedactorDetailTest(TestCase):
    def setUp(self):
        self.redactor = Redactor.objects.create(
            username="redactor1",
            first_name="John",
            last_name="Doe",
            years_of_experience=1,
        )
        self.redactor_detail_url = reverse("newspaper:redactor-detail", args=[self.redactor.pk])

    def test_login_required(self):
        response = self.client.get(self.redactor_detail_url)
        expected_redirect_url = reverse("login") + "?next=" + self.redactor_detail_url

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, expected_redirect_url)


class PrivateRedactorDetailTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_name", password="test_password"
        )
        self.client.force_login(self.user)
        self.redactor = Redactor.objects.create(
            username="redactor1", first_name="John", last_name="Doe"
        )

    def test_retrieve_redactor_detail(self):
        redactor_detail_url = reverse("newspaper:redactor-detail", args=[self.redactor.pk])
        response = self.client.get(redactor_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["redactor"], self.redactor)
        self.assertTemplateUsed(response, "newspaper/redactor_detail.html")


class PrivateRedactorUpdateTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_name", password="test_password"
        )
        self.client.force_login(self.user)
        self.redactor = Redactor.objects.create(
            username="redactor1",
            first_name="John",
            last_name="Doe",
            years_of_experience=1,
            email="testemail@gmail.com",
        )

    def test_update_redactor(self):
        redactor_update_url = reverse("newspaper:redactor-update", args=[self.redactor.pk])
        redactor_data = {
            "years_of_experience": 5,
            "email": "testemail2@gmail.com",
        }
        form = RedactorInfoUpdateForm(data=redactor_data)
        self.assertTrue(form.is_valid())
        response = self.client.post(redactor_update_url, data=form.cleaned_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, REDACTOR_LIST_URL)

        updated_redactor = Redactor.objects.get(id=self.redactor.id)
        self.assertEqual(updated_redactor.years_of_experience, 5)
        self.assertEqual(updated_redactor.email, "testemail2@gmail.com")


class PrivateRedactorDeleteTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_name", password="test_password"
        )
        self.client.force_login(self.user)
        self.redactor = Redactor.objects.create(
            username="redactor1", first_name="John", last_name="Doe"
        )

    def test_delete_redactor(self):
        redactor_delete_url = reverse("newspaper:redactor-delete", args=[self.redactor.pk])
        response = self.client.delete(redactor_delete_url)

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Redactor.objects.filter(id=self.redactor.id).exists())
        self.assertRedirects(response, REDACTOR_LIST_URL)
