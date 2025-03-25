from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from raterapi.models import Category
from django.contrib.auth.models import User





class CategoryView(ViewSet):


    def list(self, request):
        owner_only = self.request.query_params.get("owner", None)   

        try:
            # Start with all rows
            categories = Category.objects.all()

            # If `?owner=current` is in the URL
            if owner_only is not None and owner_only == "current":
                # Filter to only the current user's rocks
                categories = categories.filter(user=request.auth.user)

            serializer = CategorySerializer(categories, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single type

        Returns:
            Response -- JSON serialized type record
        """

        categories = Category.objects.get(pk=pk)
        serialized = CategorySerializer(categories)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def create(self, request):
        """Handle POST requests for rocks

        Returns:
            Response: JSON serialized representation of newly created rock
        """

        # Get an object instance of a rock type
        chosen_type = Category.objects.get(pk=request.data['type_id'])

        # Create a rock object and assign it property values
        category = Category()
        category.description = request.data['description']
        category.title = request.data['title']
        category.save()

        serialized = CategorySerializer(category, many=False)

        return Response(serialized.data, status=status.HTTP_201_CREATED)


class CategorySerializer(serializers.ModelSerializer):
    """JSON serializer"""
    class Meta:
        model = Category
        fields = ( 'name', 'description', 'created_at' )



# name = models.CharField(max_length=100, unique=True)
#     description = models.TextField(blank=True, null=True)
#     created_at = models.DateTimeField(default=timezone.now)