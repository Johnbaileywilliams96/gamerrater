from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from raterapi.models import GameReview, Game
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']



class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'title']


class ReviewSerializer(serializers.ModelSerializer):
    # Add a nested representation of the game
    game_details = GameSerializer(source='game', read_only=True)
    # Add a nested representation of the user
    user_details = UserSerializer(source='user', read_only=True)
    
    class Meta:
        model = GameReview
        fields = ['id', 'game', 'game_details', 'user', 'user_details', 'review_text', 'created_at']


class ReviewView(ViewSet):

    def list(self, request):
        owner_only = self.request.query_params.get("owner", None)   

        try:
            # Start with all rows
            reviews = GameReview.objects.all()

            # If `?owner=current` is in the URL
            if owner_only is not None and owner_only == "current":
                # Filter to only the current user's reviews
                reviews = reviews.filter(user=request.auth.user)

            serializer = ReviewSerializer(reviews, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)
            
    def retrieve(self, request, pk=None):
        """Handle GET requests for single review
        
        Returns:
            Response -- JSON serialized review
        """
        try:
            review = GameReview.objects.get(pk=pk)
            serializer = ReviewSerializer(review)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except GameReview.DoesNotExist as ex:
            return Response({'message': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def create(self, request):
        """Handle POST operations for reviews
        
        Returns:
            Response -- JSON serialized review instance
        """
        user = request.auth.user
        
        try:
            # Get the game instance
            game = Game.objects.get(pk=request.data["game"])
            
            # Create the review
            review = GameReview.objects.create(
                game=game,
                user=user,
                review_text=request.data["review_text"]
            )
            
            serializer = ReviewSerializer(review)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Game.DoesNotExist:
            return Response({'message': 'Game not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': str(ex)}, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        """Handle DELETE requests for a review
        
        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            review = GameReview.objects.get(pk=pk)
            
            # Check if the authenticated user is the owner of the review
            if review.user.id != request.auth.user.id:
                return Response(
                    {'message': 'You cannot delete a review that is not yours'}, 
                    status=status.HTTP_403_FORBIDDEN
                )
                
            review.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except GameReview.DoesNotExist:
            return Response({'message': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)

