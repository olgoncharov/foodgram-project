from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from modules.purchases.models import PurchaseRecipe
from modules.recipes.models import FavoriteRecipe, Foodstuff
from modules.users.models import Subscription


class FoodstuffSerializer(serializers.ModelSerializer):
    dimension = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Foodstuff
        fields = ('name', 'dimension')


class FavoriteRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = FavoriteRecipe
        fields = '__all__'

    def to_internal_value(self, data):
        data['user'] = self.context['request'].user.pk
        return super().to_internal_value(data)

    def validate(self, data):
        if data['user'] == data['recipe'].author:
            raise ValidationError(
                'Невозможно добавлять собственные рецепты в избранное'
            )
        return data


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = '__all__'

    def to_internal_value(self, data):
        data['follower'] = self.context['request'].user.pk
        return super().to_internal_value(data)

    def validate(self, data):
        if data['follower'] == data['following']:
            raise ValidationError('Невозможно подписаться на самого себя')
        return data


class PurchaseRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = PurchaseRecipe
        fields = '__all__'

    def to_internal_value(self, data):
        data['user'] = self.context['request'].user.pk
        return super().to_internal_value(data)
