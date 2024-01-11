from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
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


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.redactor = Redactor.objects.create(username='test_redactor')
        self.topic = Topic.objects.create(name='Test Topic')
        self.newspaper = Newspaper.objects.create(
            title='Test Newspaper',
            content='Some test content.',
            topic=self.topic
        )

    def test_login_view(self):
        response = self.client.post(reverse('newspaper_agency:login'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_register_user_view(self):
        response = self.client.post(reverse('newspaper_agency:register'), {'username': 'newuser', 'password1': 'newpassword', 'password2': 'newpassword'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('newspaper_agency:register-success'))

    def test_index_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('newspaper_agency:index'))
        self.assertEqual(response.status_code, 200)

    def test_redactor_list_view(self):
        response = self.client.get(reverse('newspaper_agency:redactor-list'))
        self.assertEqual(response.status_code, 200)

    def test_topic_list_view(self):
        response = self.client.get(reverse('newspaper_agency:topic-list'))
        self.assertEqual(response.status_code, 200)

    def test_newspaper_list_view(self):
        response = self.client.get(reverse('newspaper_agency:newspaper-list'))
        self.assertEqual(response.status_code, 200)