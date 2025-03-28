from django.shortcuts import render, redirect
from .models import Recipe, Topic, Rating
from .forms import RecipeForm
import math
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse


def home(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    pgNr = int(request.GET.get('pgNr')) if request.GET.get('pgNr') is not None else 0
    sortdir = {"Auf": "", "Ab": "-"}[request.GET.get('srtdir')] if request.GET.get('srtdir') is not None else ""
    sortval = request.GET.get('srtval')

    max_recipes = Recipe.objects.count()
    recipes_latest = Recipe.objects.all()[:6]

    if len(q) == 0:
        recipes_filter = Recipe.objects.all()
    else:
        recipes_filter = Recipe.objects.filter(
            Q(topic__name__icontains=q) |
            Q(name__icontains=q) |
            Q(ingredients__icontains=q)
        ).distinct()

    topics = Topic.objects.all()
    recipes_count = recipes_filter.count()

    if sortval is not None:
        recipes_filter = recipes_filter.order_by(sortdir + sortval).distinct()

    page_size = 50
    num_pages = math.ceil(recipes_count/page_size)
    pgNr = min(max(0, pgNr), num_pages - 1)
    recipes = recipes_filter[pgNr*page_size:(pgNr+1)*page_size] if num_pages > 0 else []

    recipe_best = None
    if num_pages > 0:
        rating_values = [r.rating_mean for r in recipes]
        recipe_best = recipes[rating_values.index(max(rating_values))]

    context = {"recipes": recipes,
               "recipes_count": recipes_count, "max_recipes": max_recipes,
               "pgNr": pgNr, "num_pages": num_pages, "iter_pages": [i for i in range(num_pages)],
               "topics": topics,
               "recipes_latest": recipes_latest, "recipe_best": recipe_best}
    return render(request, 'recipes_app/home.html', context)


def recipe(request, pk):
    recipe_from_key = Recipe.objects.get(id=pk)
    # recipe_fields = {getattr(recipe_from_key, field.name) for field in recipe_from_key._meta.get_fields() if hasattr(recipe_from_key, field.name)}
    recipe_topics = recipe_from_key.topic.all()
    persons_default = recipe_from_key.persons
    required_persons = int(request.GET.get("persons")) if request.GET.get("persons") is not None else persons_default
    recompute_persons = True if request.GET.get("persons") is not None else False

    ingredients_lines = [x.replace('\t', ' ') for x in recipe_from_key.ingredients.split('\n')]
    ingredients_formated = []
    for x in ingredients_lines:
        if len(x) <= 0:
            ingredients_formated.append((' ', ' '))
        elif x[0].isdigit():
            temp_val = x.split(' ')
            temp_calc = temp_val[0].replace(',', '.')
            if recompute_persons:
                temp_calc = float(temp_calc)/float(persons_default)*float(required_persons)
                temp_calc = "{:.5f}".format(temp_calc).rstrip('0').rstrip('.')
            ingredients_formated.append((temp_calc, " ".join(temp_val[1:])))
        else:
            ingredients_formated.append((' ', x))

    if request.method == 'POST' and request.user.is_authenticated:
        stars = int(request.POST.get("stars")) if request.POST.get("stars") is not None else 0
        body = request.POST.get("body")
        if stars > 0:
            ratings = recipe_from_key.rating_set.all()
            has_rated = False
            for r in ratings:
                if request.user == r.user:
                    r.stars = stars
                    r.body = body
                    r.save()
                    has_rated = True
                    continue
            if not has_rated:
                Rating.objects.create(
                    user=request.user,
                    recipe=recipe_from_key,
                    stars=stars,
                    body=body,
                )

    ratings = recipe_from_key.rating_set.all()
    recipe_from_key.rating_count = ratings.count()
    recipe_from_key.rating_mean = sum([r.stars for r in ratings])/float(ratings.count() if ratings.count() > 0 else 1.0)
    recipe_from_key.save(update_fields=['rating_mean', 'rating_count'])

    context = {"recipe": recipe_from_key,  "ingredients_formated": ingredients_formated,
               "required_persons": required_persons, "recipe_topics": recipe_topics, "ratings": ratings}
    return render(request, 'recipes_app/recipe.html', context)


@login_required(login_url='user-login-required')
def createRecipe(request):
    topics = Topic.objects.all()

    if request.method == 'POST':

        form = RecipeForm(request.POST, request.FILES)

        if form.is_valid():
            recipe_saved = form.save()

            recipe_saved.owner = request.user
            recipe_saved.save()

            return redirect('home')
    else:
        form = RecipeForm()

    context = {'form': form, 'topics': topics, "title_of_form": "Neues Rezept"}
    return render(request, 'recipes_app/recipe_form.html', context)


def updateRecipe(request, pk):
    recipe = Recipe.objects.get(id=pk)

    if request.user != recipe.owner:
        return HttpResponse('Fehlende Berechtigung! Bitte wenden Sie sich and den Administrator.')

    form = RecipeForm(instance=recipe)
    topics = Topic.objects.all()

    if request.method == 'POST':

        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()

        return redirect('home')

    context = {'form': form, 'topics': topics, 'recipe': recipe, "title_of_form": "Update Rezept"}
    return render(request, 'recipes_app/recipe_form.html', context)


def deleteRecipe(request, pk):
    recipe = Recipe.objects.get(id=pk)

    if request.user != recipe.owner:
        return HttpResponse('Fehlende Berechtigung! Bitte wenden Sie sich and den Administrator.')

    if request.method == 'POST':
        # recipe.topic.clear()
        recipe.delete()
        return redirect('home')

    return render(request, 'recipes_app/delete.html', {'obj': recipe})
