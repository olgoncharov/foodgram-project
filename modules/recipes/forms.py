from django import forms
from django.conf import settings
from django.forms.widgets import HiddenInput
from django.utils.functional import cached_property

from .fields import TagsChoiceField
from .models import Foodstuff, Dimension, Recipe, RecipeIngredient
from .widgets import CookingTimeInput


class RecipeForm(forms.ModelForm):
    tags = TagsChoiceField(label='Теги')

    class Meta:
        model = Recipe
        fields = ('title', 'tags', 'cooking_time', 'description', 'picture')
        widgets = {
            'cooking_time': CookingTimeInput,
        }
        labels = {
            'cooking_time': 'Время приготовления',
            'picture': 'Загрузить фото',
        }

    def __init__(self, **kwargs):
        recipe = kwargs.get('instance')
        if recipe:
            kwargs.setdefault('initial', dict())
            selected_tags = [
                tag['field'] for tag in settings.RECIPE_TAGS
                if getattr(recipe, tag['field'])
            ]
            kwargs['initial']['tags'] = selected_tags

        super().__init__(**kwargs)

    def save(self, commit=True):
        selected_tags = self.cleaned_data['tags']
        for tag in settings.RECIPE_TAGS:
            setattr(self.instance, tag['field'], tag['field'] in selected_tags)

        return super().save(commit)


class RecipeIngredientForm(forms.ModelForm):
    foodstuff_name = forms.CharField(
        max_length=256,
        widget=HiddenInput,
        required=False,
    )
    dimension = forms.CharField(
        max_length=20,
        widget=HiddenInput,
        required=False,
    )
    foodstuff = forms.ModelChoiceField(
        queryset=Foodstuff.objects.all(),
        widget=HiddenInput,
        required=False,
    )

    class Meta:
        model = RecipeIngredient
        fields = ('foodstuff', 'foodstuff_name', 'quantity', 'dimension')
        widgets = {
            'quantity': HiddenInput,
        }

    def save(self, commit=True):

        foodstuff = self.cleaned_data.get('foodstuff')
        if foodstuff:
            return super().save(commit)

        recipe_ingredient = super().save(commit=False)
        dimension, _ = Dimension.objects.get_or_create(
            name=self.cleaned_data['dimension']
        )
        foodstuff, _ = Foodstuff.objects.get_or_create(
            name=self.cleaned_data['foodstuff_name'],
            dimension=dimension
        )
        recipe_ingredient.foodstuff = foodstuff
        recipe_ingredient.save()

        return recipe_ingredient


class BaseRecipeIngredientFormSet(forms.BaseInlineFormSet):

    @cached_property
    def forms(self):
        """
        С фронта может прийти набор форм со сломанной нумерацией.
        :return:
        """
        return [
            self._construct_form(i, **self.get_form_kwargs(i))
            for i in range(max(self.total_form_count(), self.initial_form_count()))
        ]
