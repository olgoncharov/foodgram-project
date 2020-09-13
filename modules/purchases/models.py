from django.contrib.auth import get_user_model
from django.db import models

from modules.recipes.models import Recipe

User = get_user_model()


class PurchaseRecipe(models.Model):
    """Рецепт, добавленный в список покупок."""

    user = models.ForeignKey(
        User,
        related_name='purchase_recipes',
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='purchases',
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Рецепт в списке покупок'
        verbose_name_plural = 'Список покупок'
        unique_together = ('user', 'recipe')

    def __str__(self):
        return f'{self.user} - {self.recipe}'
