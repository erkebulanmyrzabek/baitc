from django.shortcuts import render, get_object_or_404
from shop.models import Product
from rest_framework import viewsets, generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ProductCategory, Transaction, DigitalAsset
from .serializers import (
    ProductSerializer, ProductCategorySerializer, TransactionSerializer,
    DigitalAssetSerializer, ProductCreateSerializer, TransactionCreateSerializer,
    DigitalAssetCreateSerializer
)

# Create your views here.
def shop_view(request):
    product = Product.objects.all()

    context = {
        'product': product,
    }

    return render(request, 'shop.html', context)

class ProductViewSet(viewsets.ModelViewSet):
    """
    API для работы с товарами.
    """
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        queryset = Product.objects.all()
        product_type = self.request.query_params.get('product_type', None)
        category_id = self.request.query_params.get('category_id', None)
        
        if product_type:
            queryset = queryset.filter(product_type=product_type)
        
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        return queryset
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ProductCreateSerializer
        return ProductSerializer

class ProductCategoryViewSet(viewsets.ModelViewSet):
    """
    API для работы с категориями товаров.
    """
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer

class TransactionViewSet(viewsets.ModelViewSet):
    """
    API для работы с транзакциями.
    """
    serializer_class = TransactionSerializer
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Transaction.objects.all()
        return Transaction.objects.filter(user=self.request.user)

class DigitalAssetViewSet(viewsets.ModelViewSet):
    """
    API для работы с цифровыми активами.
    """
    serializer_class = DigitalAssetSerializer
    
    def get_queryset(self):
        queryset = DigitalAsset.objects.all()
        asset_type = self.request.query_params.get('asset_type', None)
        
        if asset_type:
            queryset = queryset.filter(asset_type=asset_type)
        
        return queryset
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return DigitalAssetCreateSerializer
        return DigitalAssetSerializer

class BuyProductView(APIView):
    """
    API для покупки товара.
    """
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        user = request.user
        quantity = request.data.get('quantity', 1)
        shipping_address = request.data.get('shipping_address', '')
        
        # Проверки
        if not product.is_available:
            return Response({"error": "Товар недоступен для покупки"}, status=status.HTTP_400_BAD_REQUEST)
        
        if product.stock > 0 and quantity > product.stock:
            return Response({"error": f"Недостаточно товара на складе. Доступно: {product.stock}"}, status=status.HTTP_400_BAD_REQUEST)
        
        total_price = product.price * quantity
        
        if user.coin < total_price:
            return Response({"error": "Недостаточно кристаллов для покупки"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Списываем кристаллы у пользователя
        user.coin -= total_price
        user.save()
        
        # Создаем транзакцию
        transaction = Transaction.objects.create(
            user=user,
            product=product,
            quantity=quantity,
            total_price=total_price,
            status='completed',
            shipping_address=shipping_address
        )
        
        # Если это премиум-статус, активируем его
        if product.product_type == 'premium':
            user.is_premium = True
            user.save()
        
        # Уменьшаем количество товара на складе
        if product.stock > 0:
            product.stock -= quantity
            product.save()
        
        return Response({
            "success": "Товар успешно куплен",
            "transaction": TransactionSerializer(transaction).data
        }, status=status.HTTP_200_OK)

class BuyDigitalAssetView(APIView):
    """
    API для покупки цифрового актива.
    """
    def post(self, request, asset_id):
        asset = get_object_or_404(DigitalAsset, id=asset_id)
        user = request.user
        
        # Проверяем, есть ли уже этот актив у пользователя
        if user in asset.users.all():
            return Response({"error": "У вас уже есть этот цифровой актив"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Проверяем, хватает ли кристаллов
        if user.coin < asset.price:
            return Response({"error": "Недостаточно кристаллов для покупки"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Списываем кристаллы у пользователя
        user.coin -= asset.price
        user.save()
        
        # Добавляем актив пользователю
        asset.users.add(user)
        
        return Response({
            "success": "Цифровой актив успешно куплен",
            "asset": DigitalAssetSerializer(asset).data
        }, status=status.HTTP_200_OK)

class MyTransactionsView(generics.ListAPIView):
    """
    API для просмотра своих транзакций.
    """
    serializer_class = TransactionSerializer
    
    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

class MyDigitalAssetsView(generics.ListAPIView):
    """
    API для просмотра своих цифровых активов.
    """
    serializer_class = DigitalAssetSerializer
    
    def get_queryset(self):
        return DigitalAsset.objects.filter(users=self.request.user)