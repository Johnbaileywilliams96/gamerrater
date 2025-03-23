from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from raterapi.models import Game
from django.contrib.auth.models import User





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



class GameSerializer(serializers.ModelSerializer):
    """JSON serializer"""
    class Meta:
        model = Game
        fields = ( 'id', 'title', 'description', 'designer', 'created_at', )



# model": "raterapi.game",
#       "pk": 1,
#       "fields": {
#         "title": "Gloomhaven",
#         "description": "Gloomhaven is a cooperative game of tactical combat, battling monsters and advancing a player's own individual goals in a persistent and changing world that is ideally played over many game sessions.",
#         "designer": "Isaac Childres",
#         "year_released": 2017,
#         "min_players": 1,
#         "max_players": 4,
#         "estimated_play_time": 120,
#         "age_recommendation": 14,
#         "created_by": 1,
#         "created_at": "2023-03-10T14:30:00Z",
#         "updated_at": "2023-03-10T14:30:00Z"
#       }