from django.conf import settings
from django.forms import MultipleChoiceField

from .widgets import TagsSelectMultiple


class TagsChoiceField(MultipleChoiceField):
    widget = TagsSelectMultiple

    def __init__(self, **kwargs):
        kwargs['choices'] = tuple(
            (tag['field'], tag['title']) for tag in settings.RECIPE_TAGS
        )
        super().__init__(**kwargs)
