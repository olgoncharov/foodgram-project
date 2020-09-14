from django.views import generic

from modules.recipes.models import Recipe


class RecipeDetailView(generic.DetailView):
    """Контроллер страницы рецепта."""

    model = Recipe
    template_name = 'recipe.html'

    def get_queryset(self):
        return Recipe.objects.get_recipes_for_user(self.request.user)
