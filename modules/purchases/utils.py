from django.db.models import Sum, F

from modules.recipes.models import RecipeIngredient


def get_detailed_shop_list(user):
    """
    Возвращает строку с перечнем ингредиентов к покупке на основе
    добавленных в корзину рецептов.

    :param user: пользователь, для которого формируется список покупок
    :return: string, многострочная строка в формате:
     <имя продукта> (<единица измерения>) - <количество>

    Пример результата:

    Фарш (баранина и говядина) (г) — 600
    Сыр плавленый (г) — 200
    Лук репчатый (г) — 50
    Картофель (г) — 1000
    """

    ingredients = (
        RecipeIngredient.objects.select_related(
            'foodstuff',
            'foodstuff__dimension'
        ).filter(
            recipe__purchases__user=user
        ).values(
            name=F('foodstuff__name'),
            dimension=F('foodstuff__dimension__name')
        ).annotate(
            total_quantity=Sum('quantity')
        )
    )

    return '\n'.join([
        f'{item["name"]} ({item["dimension"]}) - {item["total_quantity"]}'
        for item in ingredients
    ])
