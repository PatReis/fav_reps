from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from user_app.models import User


class Topic(models.Model):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Recipe(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    name = models.CharField(max_length=500)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    topic = models.ManyToManyField(Topic, blank=True)

    persons = models.IntegerField()
    ingredients = models.TextField(null=True, blank=True)
    steps = models.TextField(null=True, blank=True)

    tips = models.TextField(null=True, blank=True)
    reference = models.TextField(null=True, blank=True)
    nutrients_person = models.FloatField(null=True, blank=True, default=0.0)
    nutrients_table = models.TextField(null=True, blank=True)
    expected_time_total = models.FloatField(null=True, blank=True, default=0.0)
    expected_time_work = models.FloatField(null=True, blank=True, default=0.0)
    expected_time_bake = models.FloatField(null=True, blank=True, default=0.0)
    expected_time_rest = models.FloatField(null=True, blank=True, default=0.0)
    difficulty = models.IntegerField(null=True, blank=True, default=0)
    image_meal = models.ImageField(blank=True, upload_to="recipes")
    rating = models.FloatField(blank=True, default=0.0)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name
