from django.contrib import admin

from . import models


class FoodstuffAdmin(admin.ModelAdmin):
    list_display = ('name', 'dimension')
    search_fields = ('name',)


class RecipeIngredientInline(admin.TabularInline):
    model = models.RecipeIngredient


class RecipeAdmin(admin.ModelAdmin):

    inlines = (RecipeIngredientInline,)
    list_display = ('title', 'author', 'count_of_favorites')
    search_fields = ('title',)
    list_filter = ('author', 'breakfast', 'lunch', 'dinner')

    def count_of_favorites(self, obj):
        """Количество добавлений рецепта в избранное."""

        return obj.favorites.count()


admin.site.register(models.Dimension)
admin.site.register(models.Foodstuff, FoodstuffAdmin)
admin.site.register(models.Recipe, RecipeAdmin)
admin.site.register(models.FavoriteRecipe)
