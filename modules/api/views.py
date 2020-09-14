from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.status import is_success
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin

from modules.purchases.models import PurchaseRecipe
from modules.recipes.models import FavoriteRecipe, Foodstuff
from modules.users.models import Subscription
from .serializers import (FavoriteRecipeSerializer, FoodstuffSerializer,
                          SubscriptionSerializer, PurchaseRecipeSerializer)


class FoodstuffListView(ListAPIView):
    """
    Возвращает список продуктов, удовлетворяющих поисковому запросу при
    подборе ингредиентов в рецепте.
    """

    permission_classes = (AllowAny,)
    queryset = Foodstuff.objects.all()
    serializer_class = FoodstuffSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class FavoriteViewSet(CreateModelMixin, DestroyModelMixin, GenericViewSet):
    """
    Вьюсет для работы с избранным. Доступные действия:
    1) добавление рецепта в избранное
    2) удаление рецепта из избранного
    """

    serializer_class = FavoriteRecipeSerializer
    lookup_field = 'recipe'

    def get_queryset(self):
        return FavoriteRecipe.objects.filter(user=self.request.user)


class SubscriptionViewSet(CreateModelMixin, DestroyModelMixin, GenericViewSet):
    """
    Вьюсет для работы с подписками. Доступные действия:
    1) подписаться на автора
    2) отписаться от автора
    """

    serializer_class = SubscriptionSerializer
    lookup_field = 'following'

    def get_queryset(self):
        return Subscription.objects.filter(follower=self.request.user)


class PurchaseViewSet(CreateModelMixin, DestroyModelMixin, GenericViewSet):
    """
    Вьюсет для работы с покупками. Доступные действия:
    1) добавить рецепт в список покупок
    2) удалить рецепт из списка покупок
    """

    serializer_class = PurchaseRecipeSerializer
    lookup_field = 'recipe'

    def get_queryset(self):
        return PurchaseRecipe.objects.filter(user=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        response.data = {
            'success': is_success(response.status_code)
        }
        return response
