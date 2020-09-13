from django.views import generic

from modules.recipes.models import Recipe


class RecipeDetailView(generic.DetailView):
    """Контроллер страницы рецепта."""

    model = Recipe
    template_name = 'recipe.html'

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Recipe.objects.all().get_recipes_for_auth_user(user)
        return super().get_queryset()
