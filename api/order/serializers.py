from rest_framework import serializers
from apps.order.models import Order, Cart, CartItem, Wishlist


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.title', read_only=True)
    variant_name = serializers.CharField(source='variant.name', read_only=True)
    variant_percent = serializers.IntegerField(source='variant.percent', read_only=True)
    product_price_uzs = serializers.IntegerField(source='product_image.price_uzs', read_only=True)

    class Meta:
        model = CartItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    order_items = CartItemSerializer(many=True, read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    user_phone_number = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'user_id', 'first_name', 'last_name', 'user_phone_number', 'phone_number', 'status', 'order_items')
        extra_kwargs = {
            'user': {'read_only': True},
            'phone_number': {'read_only': True},
        }

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance


class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = '__all__'
