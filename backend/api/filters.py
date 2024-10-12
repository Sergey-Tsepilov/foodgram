from django_filters import rest_framework
from django_filters.rest_framework import FilterSet

from recipes.models import Ingredient, Recipe, Tag


class IngredientFilterSet(FilterSet):
    """Фильтр для ингредиентов."""

    name = rest_framework.CharFilter(lookup_expr='startswith')

    class Meta:
        """Мета."""

        model = Ingredient
        fields = ('name',)


class RecipeFilterSet(FilterSet):
    """Фильтр для рецептов."""

    tags = rest_framework.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug',
    )
    is_favorited = rest_framework.NumberFilter(method='filter_is_favorited')
    is_in_shopping_cart = rest_framework.NumberFilter(
        method='filter_is_in_shopping_cart'
    )

    def filter_is_favorited(self, queryset, name, value):
        """Фильтр по избранным рецептам."""
        if value == 1:
            user = self.request.user
            return queryset.filter(favoriterecipes__user_id=user.id)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        """Фильтр по рецептам в корзине."""
        if value == 1:
            user = self.request.user
            return queryset.filter(shoppingcarts__user_id=user.id)
        return queryset

    class Meta:
        """Мета."""

        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')
