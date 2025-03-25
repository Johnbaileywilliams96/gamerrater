from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from raterapi.models import GameCategory
from django.contrib.auth.models import User
from django.utils import timezone





class GameCategoryView(ViewSet):


    def list(self, request):
        owner_only = self.request.query_params.get("owner", None)   

        try:
            # Start with all rows
            gamecategories = GameCategory.objects.all()

            # If `?owner=current` is in the URL
            if owner_only is not None and owner_only == "current":
                # Filter to only the current user's rocks
                gamecategories = gamecategories.filter(user=request.auth.user)

            serializer = GameCategorySerializer(gamecategories, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single type

        Returns:
            Response -- JSON serialized type record
        """

        gamecategories = GameCategory.objects.get(pk=pk)
        serialized = GameCategorySerializer(gamecategories)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def create(self, request):
        """Handle POST requests for game categories

        Returns:
            Response: JSON serialized representation of newly created game category
        """
        # Create a game category object and assign property values
        game_category = GameCategory()
        game_category.game_id = request.data['game']
        game_category.category_id = request.data['category']
        game_category.created_by = request.auth.user
        game_category.created_at = request.data.get('created_at', timezone.now())
        game_category.save()

        serialized = GameCategorySerializer(game_category, many=False)
        return Response(serialized.data, status=status.HTTP_201_CREATED)

class GameCategorySerializer(serializers.ModelSerializer):
    """JSON serializer"""
    class Meta:
        model = GameCategory
        fields = ( 'game', 'category', 'created_by', 'created_at' )


#    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='categories')
#     category = models.ForeignKey(GameCategory, on_delete=models.CASCADE, related_name='games')
#     created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_categories')
#     created_at = models.DateTimeField(default=timezone.now)
