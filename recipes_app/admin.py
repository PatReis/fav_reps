from django.contrib import admin
from .models import Topic, Recipe, Rating


admin.site.register(Topic)
admin.site.register(Recipe)
admin.site.register(Rating)
