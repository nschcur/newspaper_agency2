from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Redactor, Topic, Newspaper
from newspaper_agency2.settings import AUTH_USER_MODEL


class RedactorModelTest(TestCase):

    def test_redactor_creation(self):
        redactor = Redactor.objects.create(username='testuser', password='testpassword')
        self.assertEqual(str(redactor), 'testuser: ')

    def test_redactor_years_of_experience_validation(self):
        # Test that years_of_experience should be between 1 and 50
        redactor = Redactor(username='testuser', password='testpassword', years_of_experience=55)
        with self.assertRaises(ValidationError):
            redactor.full_clean()


class TopicModelTest(TestCase):

    def test_topic_creation(self):
        topic = Topic.objects.create(name='Science')
        self.assertEqual(str(topic), 'Science')


class NewspaperModelTest(TestCase):

    def setUp(self):
        self.topic = Topic.objects.create(name='Science')
        self.redactor = Redactor.objects.create(username='redactor', password='password')

    def test_newspaper_creation(self):
        newspaper = Newspaper.objects.create(
            title='Test Newspaper',
            content='Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
            topic=self.topic
        )
        newspaper.publishers.add(self.redactor)

        self.assertEqual(str(newspaper), 'title: Test Newspaper, topic: Science, published date: ')

    def test_newspaper_additional_topics(self):
        newspaper = Newspaper.objects.create(
            title='Test Newspaper',
            content='Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
            topic=self.topic
        )
        newspaper.additional_topics.add(Topic.objects.create(name='Technology'))

        self.assertEqual(newspaper.additional_topics.count(), 1)
