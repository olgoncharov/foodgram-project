from django.urls import path

from .views import DeletePurchaseRecipeView, ShopListView, download_shop_list


urlpatterns = [
    path('shoplist/', ShopListView.as_view(), name='shoplist'),
    path(
        'shoplist/<int:pk>/',
        DeletePurchaseRecipeView.as_view(),
        name='shoplist_delete'
    ),
    path('shoplist/download/', download_shop_list, name='shoplist_download')
]