from django.db import transaction
from django.forms import inlineformset_factory
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import ModelFormMixin

from modules.recipes.forms import (RecipeForm, RecipeIngredientForm,
                                   BaseRecipeIngredientFormSet)
from modules.recipes.models import Recipe, RecipeIngredient


class RecipeModelFormMixin(ModelFormMixin):
    """
    Расширяет стандартный миксин, реализуя функционал по работе
    с ингредиентами рецепта.
    """

    form_class = RecipeForm
    model = Recipe

    def get_ingredients_formset_class(self):
        return inlineformset_factory(
            parent_model=self.model,
            model=RecipeIngredient,
            formset=BaseRecipeIngredientFormSet,
            fk_name='recipe',
            form=RecipeIngredientForm,
            extra=0,
            can_delete=False,
        )

    def get_ingredients_formset(self):
        """
        Возвращает набор форм для списка ингредиентов рецепта.
        """

        formset_class = self.get_ingredients_formset_class()
        if self.request.method in ('POST', 'PUT'):
            formset = formset_class(
                data=self.request.POST, instance=self.object
            )

            # если пользователь на фронте удаляет ранее добавленные
            # ингредиенты, то в нумерации форм образуются дыры, что приводит
            # к появлению пустых форм в формсете
            # поэтому проверяем каждую форму в наборе и удаляем ненужные
            idx = 0
            initial_forms_count = 0
            while idx < len(formset.forms):
                form = formset.forms[idx]
                if form.is_valid():
                    idx += 1
                    if form.instance.pk is not None:
                        initial_forms_count = idx
                else:
                    del formset.forms[idx]
            formset.management_form.cleaned_data['TOTAL_FORMS'] = idx
            formset.management_form.cleaned_data['INITIAL_FORMS'] = initial_forms_count
        else:
            formset = formset_class(instance=self.object)

        return formset

    def validate_ingredients(self, formset):

        errors = []

        if not formset.forms:
            errors.append('Не указаны ингредиенты')
            return errors

        if not formset.is_valid():
            for error in formset.errors:
                errors.append(error.as_text())

        return errors

    def delete_ingredients_after_save(self, formset):
        """
        Удаляет ингредиенты рецепта, которые были удалены
        пользователем в форме редактирования.
        """

        self.object.ingredient_details.exclude(
            pk__in=[form.instance.pk for form in formset]
        ).delete()

    def form_valid(self, form):
        """
        Переопределяет поведение после валидации формы рецепта:
            1) сохраняет объект рецепта
            2) производит валидацию списка ингредиентов
            3) сохраняет список ингредиентов рецепта
        """

        transaction.set_autocommit(False)

        is_new = self.object is None

        form.instance.author = self.request.user
        self.object = form.save()

        ingredients_formset = self.get_ingredients_formset()
        ingredients_errors = self.validate_ingredients(ingredients_formset)
        if not ingredients_errors:
            ingredients_formset.save()
            self.delete_ingredients_after_save(ingredients_formset)
            transaction.commit()
            return super().form_valid(form)

        transaction.rollback()
        if is_new:
            self.object = None
        return self.form_invalid(form, ingredients_errors)

    def form_invalid(self, form, ingredients_errors=None):
        context = self.get_context_data(form=form)
        context['ingredients_errors'] = ingredients_errors
        return self.render_to_response(context)

    def get_success_url(self):
        return reverse_lazy('recipe', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        if 'ingredients_formset' not in kwargs:
            kwargs['ingredients_formset'] = self.get_ingredients_formset()
        return super().get_context_data(**kwargs)


class AuthorOrAdminAccessMixin:
    """
    Миксин, ограничивающий доступ к странице всем пользователям, за исключением
    автора рецепта и администратора.
    """

    def get(self, request, *args, **kwargs):

        if not request.user.is_superuser:
            recipe = self.get_object()
            if recipe.author != request.user:
                return redirect('recipe', **kwargs)

        return super().get(request, *args, **kwargs)
