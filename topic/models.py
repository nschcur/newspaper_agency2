from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

from newspaper_agency2 import settings


class Redactor(AbstractUser):

    years_of_experience = models.IntegerField(
        blank=True, null=True,
        validators=[MaxValueValidator(50), MinValueValidator(1)]
    )

    class Meta:
        ordering = ("id", )

    def __str__(self):
        return f"{self.username}: {self.first_name} {self.last_name}"


class Topic(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ("name", )

    def __str__(self):
        return self.name


class Newspaper(models.Model):
    title = models.CharField(max_length=255, unique=True)
    content = models.TextField()
    published_date = models.DateField(auto_now_add=True)

    topic = models.ForeignKey(
        Topic,
        on_delete=models.DO_NOTHING,
        related_name="subjects"
    )

    publishers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="newspaper_redactors",
    )
    additional_topics = models.ManyToManyField(
        Topic,
        related_name="topics",
    )

    class Meta:
        ordering = ("published_date", )

    def __str__(self):
        return (f"title: {self.title},"
                f"topic: {self.topic}, published date: {self.published_date}")
