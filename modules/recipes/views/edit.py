from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import ProcessFormView

from .mixins import AuthorOrAdminAccessMixin, RecipeModelFormMixin
from ..models import Recipe


class BaseCreateRecipeView(RecipeModelFormMixin, ProcessFormView):

    def get(self, request, *args, **kwargs):
        self.object = None
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        return super().post(request, *args, **kwargs)


class BaseUpdateRecipeView(RecipeModelFormMixin, ProcessFormView):

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)


class CreateRecipeView(LoginRequiredMixin,
                       SingleObjectTemplateResponseMixin,
                       BaseCreateRecipeView):
    """Контроллер создания нового рецепта."""

    template_name = 'recipe_edit_form.html'


class UpdateRecipeView(LoginRequiredMixin,
                       AuthorOrAdminAccessMixin,
                       SingleObjectTemplateResponseMixin,
                       BaseUpdateRecipeView):
    """Контроллер редактирования существующего рецепта."""

    template_name = 'recipe_edit_form.html'


class DeleteRecipeView(LoginRequiredMixin,
                       AuthorOrAdminAccessMixin,
                       generic.DeleteView):
    """Контроллер удаления рецепта."""

    model = Recipe
    success_url = reverse_lazy('index')
    http_method_names = ['post']
