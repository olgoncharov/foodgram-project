from .edit import CreateRecipeView, UpdateRecipeView, DeleteRecipeView
from .error_handlers import page_not_found, server_error
from .detail import RecipeDetailView
from .object_lists import (AuthorRecipeListView, FavoriteListView,
                           FollowListView, IndexView)
