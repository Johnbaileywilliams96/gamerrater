from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from raterapi.models import GameRating, Game
from django.contrib.auth.models import User

class RatingView(ViewSet):
    def list(self, request):
        user_only = self.request.query_params.get("user", None)   

        try:
            # Start with all rows
            ratings = GameRating.objects.all()

            # If `?user=current` is in the URL
            if user_only is not None and user_only == "current":
                # Filter to only the current user's ratings
                ratings = ratings.filter(user=request.auth.user)

            serializer = RatingSerializer(ratings, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single rating

        Returns:
            Response -- JSON serialized rating record
        """
        try:
            rating = GameRating.objects.get(pk=pk)
            serialized = RatingSerializer(rating)
            return Response(serialized.data, status=status.HTTP_200_OK)
        except GameRating.DoesNotExist:
            return Response({'message': 'Rating not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        """Handle POST requests for game ratings

        Returns:
            Response: JSON serialized representation of newly created rating
        """
        try:
            # Get the game instance
            game = Game.objects.get(pk=request.data['game_id'])
            
            # Create a new rating
            rating = GameRating()
            rating.game = game
            rating.user = request.auth.user
            rating.rating = request.data['rating']
            rating.save()

            serialized = RatingSerializer(rating, many=False)
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        
        except Game.DoesNotExist:
            return Response({'message': 'Game not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return HttpResponseServerError(ex)

class RatingSerializer(serializers.ModelSerializer):
    """JSON serializer"""
    class Meta:
        model = GameRating
        fields = ('id', 'game', 'user', 'rating', 'created_at', 'updated_at')
        depth = 1  # This will include the related game and user objects in the response