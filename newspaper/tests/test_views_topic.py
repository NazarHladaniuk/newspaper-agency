from django.contrib.auth import get_user_model
from django.test import TestCase

from django.urls import reverse

from newspaper.models import Topic

TOPIC_LIST_URL = reverse("newspaper:topic-list")
TOPIC_CREATE_URL = reverse("newspaper:topic-create")


class PublicTopicListTest(TestCase):
    def test_login_required(self):
        expected_redirect_url = reverse("login") + "?next=" + TOPIC_LIST_URL
        response = self.client.get(TOPIC_LIST_URL)
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, expected_redirect_url)


class PrivateTopicListTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_name", password="test_password"
        )
        self.client.force_login(self.user)
        self.topic1 = Topic.objects.create(name="topic1")
        self.topic2 = Topic.objects.create(name="topic2")

    def test_retrieve_topic_list(self):
        response = self.client.get(TOPIC_LIST_URL)
        topics = Topic.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["topic_list"]),
            list(topics),
        )
        self.assertTemplateUsed(response, "newspaper/topic_list.html")

    def test_topic_list_search(self):
        topic_queryset = Topic.objects.filter(name__icontains="topic1")
        response = self.client.get(TOPIC_LIST_URL + "?name=topic1")

        self.assertEqual(
            list(response.context["topic_list"]),
            list(topic_queryset),
        )

        self.assertTemplateUsed(response, "newspaper/topic_list.html")

    def test_topic_list_search_empty(self):
        response = self.client.get(TOPIC_LIST_URL + "?name=abc")

        self.assertEqual(
            list(response.context["topic_list"]),
            [],
        )

        self.assertTemplateUsed(response, "newspaper/topic_list.html")


class PrivateTopicCreateTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_name", password="test_password"
        )
        self.client.force_login(self.user)

    def test_create_topic(self):
        response = self.client.post(TOPIC_CREATE_URL, {"name": "new_topic"})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, TOPIC_LIST_URL)

        topic = Topic.objects.filter(name="new_topic").first()
        self.assertIsNotNone(topic)


class PrivateTopicUpdateTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_name", password="test_password"
        )
        self.client.force_login(self.user)
        self.topic = Topic.objects.create(name="old_topic")
        self.topic_update_url = reverse("newspaper:topic-update", args=[self.topic.pk])

    def test_update_topic(self):
        updated_topic_name = "updated_topic"
        response = self.client.post(self.topic_update_url, {"name": updated_topic_name})

        self.assertEqual(response.status_code, 302)
        self.topic.refresh_from_db()
        self.assertEqual(self.topic.name, updated_topic_name)
        self.assertRedirects(response, reverse("newspaper:topic-list"))


class PrivateTopicDeleteTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_name", password="test_password"
        )
        self.client.force_login(self.user)
        self.topic = Topic.objects.create(name="topic_to_delete")
        self.topic_delete_url = reverse("newspaper:topic-delete", args=[self.topic.pk])

    def test_delete_topic(self):
        response = self.client.post(self.topic_delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("newspaper:topic-list"))

        topic_exists = Topic.objects.filter(id=self.topic.id).exists()
        self.assertFalse(topic_exists)
