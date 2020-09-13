from django.conf import settings
from django.forms.widgets import CheckboxSelectMultiple, NumberInput, Widget


TAG_COLORS = {
    tag['field']: tag['color'] for tag in settings.RECIPE_TAGS
}


class TagsSelectMultiple(CheckboxSelectMultiple):
    template_name = 'widgets/tags_multiple_input.html'
    option_template_name = 'widgets/tag_input_option.html'
    default_tag_color = 'green'

    def create_option(self, name, value, label, selected, index,
                      subindex=None, attrs=None):
        option = super().create_option(
            name, value, label, selected, index, subindex, attrs
        )
        option['color'] = TAG_COLORS.get(option['value'], self.default_tag_color)
        return option


class CookingTimeInput(NumberInput):
    template_name = 'widgets/cooking_time_input.html'
