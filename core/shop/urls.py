from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'shop'

router = DefaultRouter()
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'categories', views.ProductCategoryViewSet, basename='category')
router.register(r'transactions', views.TransactionViewSet, basename='transaction')
router.register(r'digital-assets', views.DigitalAssetViewSet, basename='digital-asset')

urlpatterns = [
    path('products/buy/<int:product_id>/', views.BuyProductView.as_view(), name='buy-product'),
    path('digital-assets/buy/<int:asset_id>/', views.BuyDigitalAssetView.as_view(), name='buy-digital-asset'),
    path('transactions/my/', views.MyTransactionsView.as_view(), name='my-transactions'),
    path('digital-assets/my/', views.MyDigitalAssetsView.as_view(), name='my-digital-assets'),
]

urlpatterns += router.urls 