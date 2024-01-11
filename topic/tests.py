from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from .forms import LoginForm, SignUpForm, NewspaperAdminForm, RedactorCreationForm
from .models import Redactor, Topic, Newspaper

class RedactorModelTest(TestCase):
    def setUp(self):
        self.redactor = Redactor.objects.create(
            username='test_redactor',
            first_name='John',
            last_name='Doe',
            years_of_experience=5
        )

    def test_redactor_str(self):
        self.assertEqual(str(self.redactor), 'test_redactor: John Doe')


class TopicModelTest(TestCase):
    def setUp(self):
        self.topic = Topic.objects.create(name='Politics')

    def test_topic_str(self):
        self.assertEqual(str(self.topic), 'Politics')


class NewspaperModelTest(TestCase):
    def setUp(self):
        self.redactor = Redactor.objects.create(
            username='test_redactor',
            first_name='John',
            last_name='Doe',
            years_of_experience=5
        )
        self.topic = Topic.objects.create(name='Politics')
        self.newspaper = Newspaper.objects.create(
            title='Breaking News',
            content='Some breaking news content.',
            published_date=timezone.now(),
            topic=self.topic
        )
        self.newspaper.publishers.add(self.redactor)

    def test_newspaper_str(self):
        expected_str = 'title: Breaking News, topic: Politics, published date: '
        self.assertTrue(expected_str in str(self.newspaper))

    def test_newspaper_publishers(self):
        self.assertEqual(self.newspaper.publishers.count(), 1)
        self.assertEqual(self.newspaper.publishers.first(), self.redactor)


class LoginFormTest(TestCase):
    def test_login_form(self):
        form_data = {'username': 'test_user', 'password': 'test_password'}
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())


class SignUpFormTest(TestCase):
    def test_signup_form(self):
        form_data = {
            'username': 'test_user',
            'email': 'test@example.com',
            'password1': 'test_password',
            'password2': 'test_password',
        }
        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid())


class NewspaperAdminFormTest(TestCase):
    def test_newspaper_admin_form(self):
        user = get_user_model().objects.create(username='test_publisher')
        form_data = {
            'title': 'Test Newspaper',
            'content': 'Some test content.',
            'topic': Topic.objects.create(name='Test Topic'),
            'publishers': [user.id],
        }
        form = NewspaperAdminForm(data=form_data)
        self.assertTrue(form.is_valid())


class RedactorCreationFormTest(TestCase):
    def test_redactor_creation_form(self):
        form_data = {
            'username': 'test_redactor',
            'password1': 'test_password',
            'password2': 'test_password',
            'years_of_experience': 5,
            'first_name': 'John',
            'last_name': 'Doe',
        }
        form = RedactorCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

