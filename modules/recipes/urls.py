from django.urls import path

from .views import (AuthorRecipeListView, CreateRecipeView, DeleteRecipeView,
                    FavoriteListView, FollowListView, IndexView,
                    RecipeDetailView, UpdateRecipeView)


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('recipe/new/', CreateRecipeView.as_view(), name='recipe_create'),
    path('recipe/<int:pk>/', RecipeDetailView.as_view(), name='recipe'),
    path('recipe/<int:pk>/edit/', UpdateRecipeView.as_view(), name='recipe_edit'),
    path('recipe/<int:pk>/delete/', DeleteRecipeView.as_view(), name='recipe_delete'),
    path('follow/', FollowListView.as_view(), name='follow'),
    path('favorite/', FavoriteListView.as_view(), name='favorite'),
    path('author/<int:author_pk>/', AuthorRecipeListView.as_view(), name='author'),
]
