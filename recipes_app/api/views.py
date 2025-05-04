from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import Recipe, Topic
from .serializers import RecipeSerializer, TopicSerializer
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


@login_required(login_url='user-login-required')
@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/recipes',
        'GET /api/topics',
        'GET /api/recipe/:id'
    ]
    return Response(routes)


@login_required(login_url='user-login-required')
@api_view(['GET'])
def getRecipes(request):
    r = request.user.recipe_set.all()
    serializer = RecipeSerializer(r, many=True)
    return Response(serializer.data)


@login_required(login_url='user-login-required')
@api_view(['GET'])
def getRecipe(request, pk):

    recipe = Recipe.objects.get(id=pk)
    if request.user != recipe.owner:
        return HttpResponse('Fehlende Berechtigung! Bitte wenden Sie sich and den Administrator.')

    serializer = RecipeSerializer(recipe, many=False)
    return Response(serializer.data)


@login_required(login_url='user-login-required')
@api_view(['GET'])
def getTopics(request):
    topics = Topic.objects.all()
    serializer = TopicSerializer(topics, many=True)
    return Response(serializer.data)

