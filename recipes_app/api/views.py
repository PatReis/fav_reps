from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import Recipe, Topic
from .serializers import RecipeSerializer, TopicSerializer


@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/recipes',
        'GET /api/topics',
        'GET /api/recipe/:id'
    ]
    return Response(routes)


@api_view(['GET'])
def getRecipes(request):
    rooms = Recipe.objects.all()
    serializer = RecipeSerializer(rooms, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getRecipe(request, pk):
    room = Recipe.objects.get(id=pk)
    serializer = RecipeSerializer(room, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def getTopics(request):
    topics = Topic.objects.all()
    serializer = TopicSerializer(topics, many=True)
    return Response(serializer.data)

