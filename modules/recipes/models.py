from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

from .managers import RecipeManager

User = get_user_model()


class Dimension(models.Model):
    """Единица измерения."""

    name = models.CharField(
        max_length=20,
        verbose_name='Наименование',
        unique=True,
    )

    class Meta:
        verbose_name = 'Единица измерения'
        verbose_name_plural = 'Единицы измерения'

    def __str__(self):
        return self.name


class Foodstuff(models.Model):
    """Продукт питания."""

    name = models.CharField(
        max_length=256,
        verbose_name='Наименование',
    )
    dimension = models.ForeignKey(
        Dimension,
        on_delete=models.CASCADE,
        related_name='foodstuffs',
        verbose_name='Единица измерения',
    )

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        unique_together = ('name', 'dimension')

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Рецепт."""

    title = models.CharField(
        max_length=256,
        verbose_name='Название рецепта',
    )
    description = models.TextField(
        verbose_name='Описание',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    breakfast = models.BooleanField(verbose_name='Завтрак')
    lunch = models.BooleanField(verbose_name='Обед')
    dinner = models.BooleanField(verbose_name='Ужин')

    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления, мин',
    )
    picture = models.ImageField(
        upload_to='recipes',
        verbose_name='Фото',
    )
    ingredients = models.ManyToManyField(
        Foodstuff,
        through='RecipeIngredient',
        through_fields=('recipe', 'foodstuff'),
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
        editable=False
    )

    objects = RecipeManager()

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-created_date']

    def __str__(self):
        return self.title

    @property
    def tags(self):
        """
        Возвращает список установленных для рецепта тегов.

        :return: список словарей с ключами:
                    * title - название тега
                    * color - цвет тега
        """

        return [
            {
                'title': tag['title'],
                'color': tag['color']
            }
            for tag in settings.RECIPE_TAGS if getattr(self, tag['field'])
        ]


class RecipeIngredient(models.Model):
    """Ингредиент рецепта."""

    recipe = models.ForeignKey(
        'Recipe',
        related_name='ingredient_details',
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )
    foodstuff = models.ForeignKey(
        Foodstuff,
        on_delete=models.CASCADE,
        verbose_name='Продукт',
    )
    quantity = models.PositiveIntegerField(
        'Количество',
        default=0
    )

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецептов'

    def __str__(self):
        return f'{self.foodstuff} {self.quantity}{self.foodstuff.dimension}'


class FavoriteRecipe(models.Model):
    """Избранное."""

    user = models.ForeignKey(
        User,
        related_name='favorites',
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='favorites',
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранное'
        unique_together = ('user', 'recipe')

    def __str__(self):
        return f'{self.user} --> {self.recipe}'
