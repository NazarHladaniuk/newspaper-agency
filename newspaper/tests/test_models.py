from django.test import TestCase

from newspaper.models import Topic, Newspaper

from django.contrib.auth import get_user_model


class Modelstest(TestCase):
    def test_topic_str(self):
        topic_str = Topic.objects.create(name="test")
        self.assertEqual(str(topic_str), topic_str.name)

    def test_redactor_str(self):
        redactor = get_user_model().objects.create_user(
            username="user",
            password="testpass12345",
            first_name="name",
            last_name="secondname",
        )
        self.assertEqual(str(redactor), f"{redactor.username} ({redactor.first_name} {redactor.last_name})")

    def test_newspaper_str(self):
        topic_str = Topic.objects.create(name="test")
        newspaper = Newspaper.objects.create(
            title="test",
            content="test content",
            topic=topic_str,
        )
        self.assertEqual(str(newspaper), newspaper.title)

    def test_create_redactor_with_experience(self):
        username = "user"
        password = "testpass12345"
        first_name = "name"
        last_name = "secondname"
        years_of_experience = 5
        redactor = get_user_model().objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            years_of_experience=years_of_experience,
        )

        self.assertEqual(redactor.years_of_experience, 5)
        self.assertTrue(redactor.check_password(password))
        self.assertEqual(redactor.username, username)
