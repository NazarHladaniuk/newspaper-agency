from django.contrib.auth import get_user_model
from django.test import TestCase

from django.urls import reverse

from newspaper.models import Newspaper, Topic

NEWSPAPER_LIST_URL = reverse("newspaper:newspaper-list")


class PublicNewspaperListTest(TestCase):
    def test_login_required(self):
        expected_redirect_url = reverse("login") + "?next=" + NEWSPAPER_LIST_URL
        response = self.client.get(NEWSPAPER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, expected_redirect_url)


class PrivateNewspaperListTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_name", password="test_password"
            )
        self.client.force_login(self.user)
        self.topic = Topic.objects.create(name="test_topic")
        self.newspaper1 = Newspaper.objects.create(
            title="washington post",
            content="test_content",
            topic_id=self.topic.id,
        )
        self.newspaper2 = Newspaper.objects.create(
            title="daily mail",
            content="test_content2",
            topic_id=self.topic.id,
        )

    def test_retrieve_newspaper_list(self):
        response = self.client.get(NEWSPAPER_LIST_URL)
        newspapers = Newspaper.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["newspaper_list"]),
            list(newspapers)
        )
        self.assertTemplateUsed(response, "newspaper/newspaper_list.html")

    def test_newspaper_list_search(self):
        newspaper_queryset = Newspaper.objects.filter(title__icontains="post")
        response = self.client.get(NEWSPAPER_LIST_URL + "?title=post")

        self.assertEqual(
            list(response.context["newspaper_list"]),
            list(newspaper_queryset),
        )

        self.assertTemplateUsed(response, "newspaper/newspaper_list.html")

    def test_newspaper_list_search_empty(self):
        response = self.client.get(NEWSPAPER_LIST_URL + "?title=cnn")

        self.assertEqual(
            list(response.context["newspaper_list"]),
            [],
        )

        self.assertTemplateUsed(response, "newspaper/newspaper_list.html")


class PublicNewspaperDetailTest(TestCase):
    def setUp(self):
        self.topic = Topic.objects.create(name="test_topic")
        self.newspaper = Newspaper.objects.create(
            title="washington post",
            content="test_content",
            topic=self.topic,
        )
        self.newspaper_detail_url = reverse("newspaper:newspaper-detail", args=[self.newspaper.pk])

    def test_login_required(self):
        expected_redirect_url = reverse("login") + "?next=" + self.newspaper_detail_url
        response = self.client.get(self.newspaper_detail_url)
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, expected_redirect_url)


class PrivateNewspaperDetailTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_name", password="test_password"
        )
        self.client.force_login(self.user)
        self.topic = Topic.objects.create(name="test_topic")
        self.newspaper = Newspaper.objects.create(
            title="washington post",
            content="test_content",
            topic_id=self.topic.id,
        )

    def test_retrieve_newspaper_detail(self):
        newspaper_detail_url = reverse("newspaper:newspaper-detail", args=[self.newspaper.pk])
        response = self.client.get(newspaper_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["newspaper"], self.newspaper)
        self.assertTemplateUsed(response, "newspaper/newspaper_detail.html")

