from collections import defaultdict
from functools import reduce

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views import generic

from modules.recipes.models import Recipe

User = get_user_model()


class BaseRecipeListView(generic.ListView):
    """Базовый класс для страницы со списком рецептов."""

    model = Recipe
    paginate_by = 6

    def get_queryset(self):
        queryset = Recipe.objects.all().get_recipes_for_user(self.request.user)

        selected_tags = self.get_selected_tags()
        if selected_tags:
            # сложное выражение из-за того, что требуется аккумулировать
            # фильтры через оператор ИЛИ, а не И
            return queryset.filter(
                reduce(lambda x, y: x | y,
                       [Q(**{tag: True}) for tag in selected_tags])
            )
        return queryset

    def get_selected_tags(self):
        """
        Извлекает из GET-параметров запроса перечень выбранных пользователем
        тегов и возвращает в виде списка. Теги передаются в виде строки и
        разделены запятыми. Например:
        https://<адрес страницы>/?tags=a,b,c

        :return: list of strings, список тегов.
        """

        tags_from_query = self.request.GET.get('tags', '')
        tags_list = []
        if tags_from_query:
            tags_list = tags_from_query.split(',')

        if set(tags_list) == {tag['field'] for tag in settings.RECIPE_TAGS}:
            # пользователь включил все возможные теги, поэтому обнуляем список
            # выбранных тегов, чтобы отключить фильтры
            return []

        return tags_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['selected_tags'] = self.get_selected_tags()
        context['available_tags'] = settings.RECIPE_TAGS
        return context


class IndexView(BaseRecipeListView):
    """Главная страница сайта со списком рецептов."""

    template_name = 'index.html'


class FavoriteListView(LoginRequiredMixin, BaseRecipeListView):
    """Страница избранного"""

    template_name = 'favorite_recipes.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_favorite=True)


class AuthorRecipeListView(BaseRecipeListView):
    """Страница с рецептами конкретного автора."""

    template_name = 'author_recipes.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author_id=self.kwargs['author_pk'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        author = get_object_or_404(User, pk=self.kwargs['author_pk'])
        context['author'] = author
        context['subscribed'] = (
            author.followers.filter(
                follower=self.request.user
            ).exists()
        )

        return context


class FollowListView(LoginRequiredMixin, generic.ListView):
    """Страница подписок."""

    paginate_by = 6
    template_name = 'my_follow.html'

    def get_queryset(self):
        return (self.request.user.subscriptions
                .select_related('following').all())

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)

        authors = [obj.following.pk for obj in context['page_obj']]
        recipes = defaultdict(list)
        for recipe in Recipe.objects.filter(author__in=authors):
            recipes[recipe.author].append(recipe)

        context['recipes'] = recipes

        return context
