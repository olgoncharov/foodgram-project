from django import template
from django.conf import settings

register = template.Library()


@register.filter
def filtering_tags_parameter(selected_tags, current_tag):
    """
    Генерирует GET-параметр в ссылке фильтрации по тегу.

    :param selected_tags: список тегов, по которым отфильтрована текущая страница
    :param current_tag: тег, для ссылки которого генерируется параметр
    :return: string

    Пример.

    Дано:
    1) в системе заведены четыре тега: a, b, c, d
    2) пользователь находится на странице `https://foodgram.ru/?tags=a,b`
       с рецептами, отфильтрованными по тегам a и b

    При рендеринге на этой странице генерируются четыре ссылки для
    фильтрации по тегам:
    1) Для тега `a` ссылка будет иметь вид `https://foodgram.ru/?tags=b`.
       Она будет исключать тег `a` из фильтра.
    2) Для тега `b` - `https://foodgram.ru/?tags=a`. Она будет исключать
       тег `b` из фильтра.
    3) Для тега `c` - `https://foodgram.ru/?tags=a,b,c`. Она будет добавлять
       тег `c` к фильтру.
    4) Для тега `d` - `https://foodgram.ru/?tags=a,b,d`. Она будет добавлять
       тег `d` к фильтру.

    При генерации ссылок функция будет для каждого тега возвращать
    значение для параметра ?tags='...'. То есть:
    filtering_tags_parameter([`a`, `b`], `a`) -->> `b`
    filtering_tags_parameter([`a`, `b`], `b`) -->> `a`
    filtering_tags_parameter([`a`, `b`], `c`) -->> `a,b,c`
    filtering_tags_parameter([`a`, `b`], `d`) -->> `a,b,d`
    """

    if selected_tags:
        target_tags = selected_tags.copy()
    else:
        target_tags = [tag['field'] for tag in settings.RECIPE_TAGS]

    if current_tag in target_tags:
        target_tags.remove(current_tag)
    else:
        target_tags.append(current_tag)

    if len(target_tags) == len(settings.RECIPE_TAGS):
        return ''

    return ','.join(target_tags)


@register.filter
def get_attribute(obj, attr):
    return getattr(obj, attr)


@register.filter
def get_by_key(obj, key):
    return obj[key]
