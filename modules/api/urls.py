from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('favorites', views.FavoriteViewSet, basename='favorite')
router.register('subscriptions', views.SubscriptionViewSet, basename='subscribe')
router.register('purchases', views.PurchaseViewSet, basename='purchase')

urlpatterns = [
    path('', include(router.urls)),
    path('foodstuff/', views.FoodstuffListView.as_view()),
]
