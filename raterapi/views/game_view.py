from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from raterapi.models import Game
from django.contrib.auth.models import User
from .category_view import CategorySerializer





class GameView(ViewSet):


    def list(self, request):
        owner_only = self.request.query_params.get("owner", None)   

        try:
            # Start with all rows
            games = Game.objects.all()

            # If `?owner=current` is in the URL
            if owner_only is not None and owner_only == "current":
                # Filter to only the current user's rocks
                games = games.filter(user=request.auth.user)

            serializer = GameSerializer(games, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single type

        Returns:
            Response -- JSON serialized type record
        """

        games = Game.objects.get(pk=pk)
        serialized = GameSerializer(games)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def create(self, request):
        """Handle POST requests for rocks

        Returns:
            Response: JSON serialized representation of newly created rock
        """

        # Get an object instance of a rock type
        chosen_type = Game.objects.get(pk=request.data['type_id'])

        # Create a rock object and assign it property values
        game = Game()
        game.user = request.auth.user
        game.description = request.data['description']
        game.title = request.data['title']
        game.designer = request.data['designer']
        game.created_at = request.data['created_at']
        game.save()

        serialized = GameSerializer(game, many=False)

        return Response(serialized.data, status=status.HTTP_201_CREATED)




class GameSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField()
    
    def get_categories(self, obj):
        game_categories = obj.categories.all()
        
        return [
            {
                'id': gc.category.id,
                'name': gc.category.name
            }
            for gc in game_categories
        ]
    
    class Meta:
        model = Game
        fields = ['id', 'title', 'description', 'designer', 'categories']


