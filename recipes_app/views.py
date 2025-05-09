from django.shortcuts import render, redirect
from .models import Recipe, Topic, Rating
from .forms import RecipeForm
import math
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from .pagination import Pagination


COOKING_DIFFICULTY_LOOKUP = {0: "einfach", 1: "mittel", 2: "schwer", 3: "profi"}


def recipes_grid(recipes_filter, request):
    q = request.GET.get('q') if request.GET.get('q') is not None else None
    pgNr = int(request.GET.get('pgNr')) if request.GET.get('pgNr') is not None else 0
    sortdir = {"Auf": "", "Ab": "-"}[request.GET.get('srtdir')] if request.GET.get('srtdir') is not None else ""
    sortval = request.GET.get('srtval')
    tpc = request.GET.get('tpc') if request.GET.get('tpc') is not None else None
    pgShow = int(request.GET.get('pgShow')) if request.GET.get('pgShow') is not None else 50

    topics = Topic.objects.all()

    if tpc is not None:
        try:
            # recipes_filter = Topic.objects.get(id=int(tpc)).recipe_set.all()
            recipes_filter = recipes_filter.filter(topic__id=int(tpc)).distinct()
        except (Topic.DoesNotExist, ValueError):
            pass

    # Start filter recipes based on query string.
    if q is not None and isinstance(q, str):
        if len(q) > 0:
            words_in_search = q.split(' ')
            for w in words_in_search:
                if len(w) == 0:
                    continue
                w = w.strip()
                recipes_filter = recipes_filter.filter(
                    Q(topic__name__icontains=w) |
                    Q(name__icontains=w) |
                    Q(owner__username__icontains=w) |
                    Q(ingredients__icontains=w)
                )
                recipes_filter = recipes_filter.distinct()

    recipes_count = recipes_filter.count()

    if sortval is not None:
        recipes_filter = recipes_filter.order_by(sortdir + sortval).distinct()

    page_size = max(min(int(pgShow), 10), 200)
    page_choices = 10
    # num_pages = math.ceil(recipes_count/page_size)
    # pgNr = min(max(0, pgNr), num_pages - 1)
    # recipes = recipes_filter[pgNr*page_size:(pgNr+1)*page_size] if num_pages > 0 else []

    browser = Pagination(recipes_count, page_size, number_page_choices=page_choices)
    pgNr = browser.valid_page(pgNr)
    num_pages = browser.number_of_pages
    recipes = browser.get_items_for_page(recipes_filter, pgNr)
    browser_context = browser.make_page_browser(pgNr)

    sort_items = [["updated", "Geändert"], ["rating_mean", "Bewertung"], ["persons", "Personen"],
                  ["created", "Erstellt"], ["difficulty", "Schwierigkeitsgrad"], ["expected_time_total", "Gesamtzeit"],
                  ["nutrients_person", "Nährwert (pro Portion)"]]

    context = {"recipes": recipes,
               "recipes_count": recipes_count,
               "pgNr": pgNr, "num_pages": num_pages,
               "topics": topics, "show_video": False,
               "sort_items": sort_items,
               "diff_lookup": COOKING_DIFFICULTY_LOOKUP}
    context.update(browser_context)
    return context


def recipes_overview(request):
    context = recipes_grid(Recipe.objects.all(), request)
    return render(request, 'recipes_app/recipes.html', context)


def recipes_video(request):
    recipes_video = Recipe.objects.exclude(video_meal__isnull=True)
    context = recipes_grid(recipes_video, request)
    context.update({"show_video": True})
    return render(request, 'recipes_app/recipes_video.html', context)


@login_required(login_url='user-login-required')
def recipes_likes(request):
    recipes_liked = request.user.likes.all()
    context = recipes_grid(recipes_liked, request)
    return render(request, 'recipes_app/recipes_likes.html', context)


def home(request):
    max_recipes = Recipe.objects.count()
    recipes_latest = Recipe.objects.all()[:6]
    recipes_best = Recipe.objects.order_by("-rating_mean")[:6]
    topics = Topic.objects.all()
    recipes = Recipe.objects.all()

    context = {
               "max_recipes": max_recipes,
               "topics": topics,
               "recipes_latest": recipes_latest,
               "recipes_best": recipes_best,
                "diff_lookup": COOKING_DIFFICULTY_LOOKUP,
    }
    return render(request, 'recipes_app/home.html', context)


def recipe(request, pk):
    recipe_from_key = Recipe.objects.get(id=pk)
    persons_default = recipe_from_key.persons
    recipe_topics = recipe_from_key.topic.all()
    required_persons = int(request.GET.get("persons")) if request.GET.get("persons") is not None else persons_default
    recompute_persons = True if request.GET.get("persons") is not None else False
    pgShow = int(request.GET.get('pgShow')) if request.GET.get('pgShow') is not None else 50
    pgNr = int(request.GET.get('pgNr')) if request.GET.get('pgNr') is not None else 0

    if request.method == 'POST' and request.user.is_authenticated:
        stars = int(request.POST.get("stars")) if request.POST.get("stars") is not None else 0
        body = request.POST.get("body")
        like = request.POST.get("like") if request.POST.get("like") is not None else None

        if like is not None:
            if like == "1":
                if request.user not in recipe_from_key.likes.all():
                    recipe_from_key.likes.add(request.user)
            else:
                if request.user in recipe_from_key.likes.all():
                    recipe_from_key.likes.remove(request.user)

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
            # Update Rating of recipes.
            ratings = recipe_from_key.rating_set.all()
            recipe_from_key.rating_count = ratings.count()
            ratings_python = [r.stars for r in ratings]
            recipe_from_key.rating_1 = sum([0.5 < r < 1.5 for r in ratings_python])
            recipe_from_key.rating_2 = sum([1.5 < r < 2.5 for r in ratings_python])
            recipe_from_key.rating_3 = sum([2.5 < r < 3.5 for r in ratings_python])
            recipe_from_key.rating_4 = sum([3.5 < r < 4.5 for r in ratings_python])
            recipe_from_key.rating_5 = sum([4.5 < r < 5.5 for r in ratings_python])
            recipe_from_key.rating_mean = sum(ratings_python) / float(ratings.count() if ratings.count() > 0 else 1.0)
            recipe_from_key.save(update_fields=['rating_mean', 'rating_count', "rating_1", "rating_2",
                                                "rating_3", "rating_4", "rating_5"])

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

    likes_count = recipe_from_key.likes.count()

    if request.user.is_authenticated:
        user_has_liked = request.user in recipe_from_key.likes.all()
    else:
        user_has_liked = None

    rating_per_cent_context = {
        "rating_%s_per_cent" % i: int(getattr(recipe_from_key, "rating_%s" % i) / float(recipe_from_key.rating_count if recipe_from_key.rating_count > 0 else 1.0) *100)
        for i in range(1, 6)
    }

    ratings = recipe_from_key.rating_set.all()
    page_size = max(min(int(pgShow), 10), 200)
    page_choices = 10
    browser = Pagination(ratings.count(), page_size, number_page_choices=page_choices)
    pgNr = browser.valid_page(pgNr)
    num_pages = browser.number_of_pages
    ratings_page = browser.get_items_for_page(ratings, pgNr)
    browser_context = browser.make_page_browser(pgNr)

    context = {"recipe": recipe_from_key,  "ingredients_formated": ingredients_formated,
               "required_persons": required_persons, "recipe_topics": recipe_topics, "ratings": ratings_page,
               "user_has_liked": user_has_liked, "likes_count": likes_count, "diff_lookup": COOKING_DIFFICULTY_LOOKUP}
    context.update(browser_context)
    context.update(rating_per_cent_context)
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

    return render(request, 'recipes_app/recipe_delete.html', {'obj': recipe})
