from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from raterapi.views import register_user, login_user
from raterapi.views import GameView, CategoryView, GameCategoryView, ReviewView, RatingView


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'games', GameView, 'game')
router.register(r'categories', CategoryView, 'category')
router.register(r'gamecategories', GameCategoryView, 'gamecategory')
router.register(r'reviews', ReviewView, 'review')
router.register(r'gameratings', RatingView, 'gamerating')


urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('admin/', admin.site.urls),
]
