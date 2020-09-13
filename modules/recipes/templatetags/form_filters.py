from django import template
from django.forms.widgets import Textarea, ClearableFileInput

register = template.Library()


@register.filter
def add_class_for_input(field):
    """
    Добавляет класс полю ввода формы в зависимости от его типа.
    """

    css = 'form__input'

    if isinstance(field.field.widget, Textarea):
        css = 'form__textarea'
    elif isinstance(field.field.widget, ClearableFileInput):
        css = ''

    return field.as_widget(attrs={"class": css})



