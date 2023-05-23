from django.test import TestCase

from newspaper.forms import RedactorCreationForm


class FormTest(TestCase):
    def test_redactor_creation_form_is_valid(self):
        form_data = {
            "username": "test1",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "email": "test@test.com",
            "years_of_experience": 4,
            "password1": "test123456",
            "password2": "test123456",
        }
        form = RedactorCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
