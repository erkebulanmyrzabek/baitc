from rest_framework import serializers
from .models import Product, ProductCategory, Transaction, DigitalAsset
from user.serializers import UserSerializer

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'name', 'description']

class ProductSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer(read_only=True)
    is_in_stock = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'image', 'category',
            'product_type', 'stock', 'is_available', 'premium_duration_days',
            'created_at', 'updated_at', 'is_in_stock'
        ]

class ProductCreateSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Product
        fields = [
            'name', 'description', 'price', 'image', 'category_id',
            'product_type', 'stock', 'is_available', 'premium_duration_days'
        ]
    
    def create(self, validated_data):
        category_id = validated_data.pop('category_id')
        product = Product.objects.create(category_id=category_id, **validated_data)
        return product

class TransactionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    product = ProductSerializer(read_only=True)
    
    class Meta:
        model = Transaction
        fields = [
            'id', 'user', 'product', 'quantity', 'total_price', 'status',
            'created_at', 'updated_at', 'shipping_address', 'tracking_number'
        ]

class TransactionCreateSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Transaction
        fields = ['product_id', 'quantity', 'shipping_address']
    
    def validate(self, data):
        user = self.context['request'].user
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)
        
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Товар не найден.")
        
        if not product.is_available:
            raise serializers.ValidationError("Товар недоступен для покупки.")
        
        if product.stock > 0 and quantity > product.stock:
            raise serializers.ValidationError(f"Недостаточно товара на складе. Доступно: {product.stock}.")
        
        if user.coin < product.price * quantity:
            raise serializers.ValidationError("Недостаточно кристаллов для покупки.")
        
        data['product'] = product
        data['total_price'] = product.price * quantity
        return data
    
    def create(self, validated_data):
        user = self.context['request'].user
        product = validated_data.pop('product')
        quantity = validated_data.get('quantity', 1)
        total_price = product.price * quantity
        
        # Списываем кристаллы у пользователя
        user.coin -= total_price
        user.save()
        
        transaction = Transaction.objects.create(
            user=user,
            product=product,
            total_price=total_price,
            status='completed',
            **validated_data
        )
        
        return transaction

class DigitalAssetSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)
    
    class Meta:
        model = DigitalAsset
        fields = ['id', 'name', 'description', 'image', 'price', 'asset_type', 'users']

class DigitalAssetCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DigitalAsset
        fields = ['name', 'description', 'image', 'price', 'asset_type'] 