import io

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView

from .models import PurchaseRecipe
from .utils import get_detailed_shop_list


class ShopListView(LoginRequiredMixin, ListView):
    """Страница списка покупок."""

    template_name = 'shop_list.html'

    def get_queryset(self):
        return self.request.user.purchase_recipes.select_related('recipe').all()


class DeletePurchaseRecipeView(DeleteView):
    """Контроллер удаления рецепта из списка покупок."""

    model = PurchaseRecipe
    http_method_names = ['post']

    def get_success_url(self):
        return reverse_lazy('shoplist')


@login_required
def download_shop_list(request):
    """Контроллер загрузки списка покупок."""

    return FileResponse(
        io.BytesIO(get_detailed_shop_list(request.user).encode('utf-8')),
        as_attachment=True,
        filename='shop_list.txt'
    )
