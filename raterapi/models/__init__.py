# First import all models that don't depend on Game
from .category import Category
from .game_category import GameCategory
# Then import Game which depends on the above
from .game import Game

from .review import GameReview

from .game_rating import GameRating