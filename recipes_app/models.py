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

    likes = models.ManyToManyField(User,  blank=True, related_name="likes")
    name = models.CharField(max_length=500)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    topic = models.ManyToManyField(Topic, blank=True)

    persons = models.IntegerField()

    ingredients = models.TextField(null=True, blank=True)
    steps = models.TextField(null=True, blank=True)
    tips = models.TextField(null=True, blank=True)

    reference = models.TextField(null=True, blank=True)
    reference_link = models.URLField(max_length=2048, null=True, blank=True)

    nutrients_person = models.FloatField(null=True, blank=True, default=0.0)
    nutrients_table = models.TextField(null=True, blank=True)

    expected_time_total = models.FloatField(null=True, blank=True, default=0.0)
    expected_time_work = models.FloatField(null=True, blank=True, default=0.0)
    expected_time_bake = models.FloatField(null=True, blank=True, default=0.0)
    expected_time_rest = models.FloatField(null=True, blank=True, default=0.0)

    difficulty = models.IntegerField(null=True, blank=True, default=0)

    image_meal = models.ImageField(blank=True, upload_to="recipes")
    video_meal = models.URLField(max_length=2048, null=True, blank=True)

    rating_mean = models.FloatField(null=True, blank=True, default=0.0)
    rating_count = models.IntegerField(null=True, blank=True, default=0)
    rating_1 = models.IntegerField(null=True, blank=True, default=0)
    rating_2 = models.IntegerField(null=True, blank=True, default=0)
    rating_3 = models.IntegerField(null=True, blank=True, default=0)
    rating_4 = models.IntegerField(null=True, blank=True, default=0)
    rating_5 = models.IntegerField(null=True, blank=True, default=0)

    @property
    def ingredients_trimmed(self):
        return self.ingredients.replace('\r\n', '\n').replace('\n', ' | ')

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    stars = models.IntegerField(default=0)
    body = models.CharField(null=True, blank=True, max_length=500)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body