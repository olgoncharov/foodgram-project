from django.apps import apps
from django.db.models import Exists, Manager, OuterRef


class RecipeManager(Manager):

    def get_recipes_for_user(self, user):
        """
        Расширенный набор записей модели рецептов, возвращаемый для
        авторизованных пользователей. Содержит дополнительные поля:
            * is_favorite - добавлен ли рецепт в избранное пользователя
            * is_purchase - добавлен ли рецепт в список покупок пользователя
            * is_subscribed - подписан ли пользователь на автора рецепта
        """

        if not user.is_authenticated:
            return self.all()

        FavoriteRecipe = apps.get_model('recipes', 'FavoriteRecipe')
        PurchaseRecipe = apps.get_model('purchases', 'PurchaseRecipe')
        Subscription = apps.get_model('users', 'Subscription')

        favorite_subquery = Exists(
            FavoriteRecipe.objects.filter(
                recipe=OuterRef('pk'),
                user=user
            )
        )
        purchases_subquery = Exists(
            PurchaseRecipe.objects.filter(
                recipe=OuterRef('pk'),
                user=user
            )
        )
        subscription_subquery = Exists(
            Subscription.objects.filter(
                following=OuterRef('author'),
                follower=user
            )
        )
        return self.all().annotate(
            is_favorite=favorite_subquery,
            is_purchase=purchases_subquery,
            is_subscribed=subscription_subquery,
        )
